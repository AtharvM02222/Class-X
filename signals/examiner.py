"""signals/examiner.py — examiner behavior modeling from marking schemes."""
import re, sys
from pathlib import Path
from collections import Counter, defaultdict
sys.path.insert(0, str(Path(__file__).parent.parent))
from blueprint import BLUEPRINT

# Marking scheme patterns
VALUE_POINT_PATTERNS = [
    r"(\d+)\s*(?:mark|marks|m)\s*(?:for|:)",
    r"\((\d+)\s*(?:mark|marks|m)\)",
    r"(\d+)\s*m\s*[-–—]",
    r"award\s*(\d+)\s*(?:mark|marks)",
]

# Common examiner expectations
EXAMINER_PREFERENCES = {
    "diagram_required": [
        "draw", "diagram", "ray diagram", "circuit diagram", "labelled diagram",
        "figure", "sketch", "illustrate",
    ],
    "formula_required": [
        "formula", "derive", "derivation", "equation", "expression",
    ],
    "example_required": [
        "give example", "with example", "for example", "examples",
        "name any", "list any", "mention any",
    ],
    "numerical_expected": [
        "calculate", "find", "numerical", "compute", "solve",
    ],
    "comparison_expected": [
        "compare", "differentiate", "distinguish", "contrast",
        "similarities", "differences",
    ],
}

def analyze_marking_scheme(text: str) -> dict:
    """Analyze a marking scheme to extract examiner patterns."""
    text_lower = text.lower()
    
    patterns = {
        "value_points_style": "standard",  # standard, detailed, brief
        "diagram_importance": 0.0,
        "formula_importance": 0.0,
        "step_marks": False,  # Whether partial marks for steps
        "common_deductions": [],
    }
    
    # Check for step-by-step marking
    if any(kw in text_lower for kw in ["step", "partial", "method mark", "even if answer is wrong"]):
        patterns["step_marks"] = True
    
    # Check diagram importance
    diagram_count = sum(1 for kw in EXAMINER_PREFERENCES["diagram_required"] if kw in text_lower)
    patterns["diagram_importance"] = min(1.0, diagram_count * 0.2)
    
    # Check formula importance
    formula_count = sum(1 for kw in EXAMINER_PREFERENCES["formula_required"] if kw in text_lower)
    patterns["formula_importance"] = min(1.0, formula_count * 0.25)
    
    # Common deduction patterns
    deduction_patterns = [
        r"deduct\s*(\d+)\s*marks?\s*(?:for|if)\s*([^.]+)",
        r"no marks?\s*(?:for|if)\s*([^.]+)",
        r"award\s*(\d+)\s*marks?\s*only\s*(?:for|if)\s*([^.]+)",
    ]
    
    for pattern in deduction_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            if isinstance(match, tuple):
                patterns["common_deductions"].append(" ".join(match)[:100])
            else:
                patterns["common_deductions"].append(match[:100])
    
    return patterns


def analyze_examiner_preferences(pdf_analysis: dict) -> dict[str, dict]:
    """Analyze examiner preferences from past papers and marking schemes."""
    preferences = {}
    
    for subject, data in pdf_analysis.items():
        questions = data.get("questions", [])
        
        chapter_prefs = {}
        
        for chapter in BLUEPRINT[subject]["chapters"]:
            if BLUEPRINT[subject]["chapters"][chapter].get("deleted"):
                continue
            
            chapter_qs = [q for q in questions if q.get("chapter") == chapter]
            
            if not chapter_qs:
                chapter_prefs[chapter] = {
                    "diagram_frequency": 0.0,
                    "numerical_frequency": 0.0,
                    "comparison_frequency": 0.0,
                    "preferred_marks": [3],  # Default
                }
                continue
            
            # Analyze question patterns
            diagram_count = 0
            numerical_count = 0
            comparison_count = 0
            mark_distribution = Counter()
            
            for q in chapter_qs:
                text = q.get("q", "").lower()
                qtype = q.get("type", "")
                marks = q.get("marks", 0)
                
                # Check for diagram requirements
                if any(kw in text for kw in EXAMINER_PREFERENCES["diagram_required"]):
                    diagram_count += 1
                
                # Check for numerical
                if any(kw in text for kw in EXAMINER_PREFERENCES["numerical_expected"]):
                    numerical_count += 1
                
                # Check for comparison
                if any(kw in text for kw in EXAMINER_PREFERENCES["comparison_expected"]):
                    comparison_count += 1
                
                # Track marks
                if marks:
                    mark_distribution[marks] += 1
            
            total = len(chapter_qs)
            chapter_prefs[chapter] = {
                "diagram_frequency": round(diagram_count / total, 3),
                "numerical_frequency": round(numerical_count / total, 3),
                "comparison_frequency": round(comparison_count / total, 3),
                "preferred_marks": [m for m, _ in mark_distribution.most_common(3)],
                "total_questions_analyzed": total,
            }
        
        preferences[subject] = chapter_prefs
    
    return preferences


def get_examiner_signal(subjects: list[str], pdf_analysis: dict) -> dict[str, dict]:
    """Get examiner preference signal for scoring.
    
    Chapters with consistent examiner patterns (always diagram, always numerical)
    are more predictable and get higher signals.
    """
    preferences = analyze_examiner_preferences(pdf_analysis)
    
    signals = {}
    for subject in subjects:
        chapter_signals = {}
        subject_prefs = preferences.get(subject, {})
        
        for chapter in BLUEPRINT[subject]["chapters"]:
            if BLUEPRINT[subject]["chapters"][chapter].get("deleted"):
                continue
            
            prefs = subject_prefs.get(chapter, {})
            
            # Higher signal for chapters with clear patterns
            signal = 0.5  # Base
            
            # Predictability bonus
            diagram_freq = prefs.get("diagram_frequency", 0)
            numerical_freq = prefs.get("numerical_frequency", 0)
            comparison_freq = prefs.get("comparison_frequency", 0)
            
            # Strong patterns increase predictability
            if diagram_freq > 0.5:
                signal += 0.15  # Diagrams are very predictable
            if numerical_freq > 0.4:
                signal += 0.15  # Numericals follow patterns
            if comparison_freq > 0.3:
                signal += 0.1
            
            # More analyzed questions = more confident signal
            analyzed = prefs.get("total_questions_analyzed", 0)
            if analyzed > 10:
                signal += 0.1
            
            chapter_signals[chapter] = round(min(1.0, max(0.0, signal)), 4)
        
        # Normalize
        if chapter_signals:
            max_sig = max(chapter_signals.values())
            if max_sig > 0:
                chapter_signals = {ch: round(s / max_sig, 4) for ch, s in chapter_signals.items()}
        
        signals[subject] = chapter_signals
    
    return signals


def get_examiner_tips(subject: str, chapter: str, pdf_analysis: dict) -> list[str]:
    """Get specific examiner tips for a chapter based on historical patterns."""
    preferences = analyze_examiner_preferences({subject: pdf_analysis.get(subject, {})})
    prefs = preferences.get(subject, {}).get(chapter, {})
    
    tips = []
    
    if prefs.get("diagram_frequency", 0) > 0.4:
        tips.append("Always include a labelled diagram - examiners expect it.")
    
    if prefs.get("numerical_frequency", 0) > 0.3:
        tips.append("Show all calculation steps - partial marks are awarded.")
    
    if prefs.get("comparison_frequency", 0) > 0.3:
        tips.append("Use a table format for comparisons when possible.")
    
    preferred_marks = prefs.get("preferred_marks", [])
    if preferred_marks:
        tips.append(f"Most common question marks: {', '.join(map(str, preferred_marks[:3]))}M")
    
    return tips
