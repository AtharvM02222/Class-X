"""signals/competency.py — NEP 2020 competency-based question mapping."""
import sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent))
from blueprint import BLUEPRINT
from config import COMPETENCY_TYPES

# Competency detection patterns
COMPETENCY_PATTERNS = {
    "knowledge": [
        "define", "state", "list", "name", "write", "mention", "recall",
        "identify", "label", "what is", "who", "when", "where",
    ],
    "understanding": [
        "explain", "describe", "compare", "contrast", "differentiate",
        "distinguish", "interpret", "summarize", "classify", "give example",
        "how does", "why is", "what happens",
    ],
    "application": [
        "apply", "solve", "calculate", "find", "determine", "compute",
        "use", "demonstrate", "show", "prove", "numerical", "word problem",
        "derive", "construct", "draw",
    ],
    "analysis": [
        "analyse", "analyze", "examine", "investigate", "relate",
        "infer", "deduce", "compare and contrast", "break down",
        "distinguish between", "what is the relationship",
    ],
    "evaluation": [
        "evaluate", "assess", "judge", "justify", "argue", "defend",
        "critique", "what would happen if", "suggest", "recommend",
        "which is better", "give your opinion", "do you agree",
    ],
}

def detect_competency(question_text: str) -> dict[str, float]:
    """Detect competency levels in a question."""
    text = question_text.lower()
    competency_scores = Counter()
    
    for competency, patterns in COMPETENCY_PATTERNS.items():
        for pattern in patterns:
            if pattern in text:
                competency_scores[competency] += 1
    
    # Normalize to probabilities
    total = sum(competency_scores.values()) or 1
    return {c: round(s / total, 3) for c, s in competency_scores.items()}


def analyze_competency_trends(pdf_analysis: dict) -> dict[str, dict]:
    """Analyze competency distribution trends from past papers."""
    trends = {}
    
    for subject, data in pdf_analysis.items():
        questions = data.get("questions", [])
        
        # Overall competency distribution
        overall_competency = Counter()
        chapter_competency = {}
        year_competency = {}
        
        for q in questions:
            chapter = q.get("chapter", "")
            year = q.get("year", 0)
            text = q.get("q", "")
            
            if not text:
                continue
            
            competencies = detect_competency(text)
            
            # Aggregate
            for comp, score in competencies.items():
                overall_competency[comp] += score
            
            # Per chapter
            if chapter:
                if chapter not in chapter_competency:
                    chapter_competency[chapter] = Counter()
                for comp, score in competencies.items():
                    chapter_competency[chapter][comp] += score
            
            # Per year
            if year:
                if year not in year_competency:
                    year_competency[year] = Counter()
                for comp, score in competencies.items():
                    year_competency[year][comp] += score
        
        # Normalize chapter competencies
        chapter_normalized = {}
        for chapter, counts in chapter_competency.items():
            total = sum(counts.values()) or 1
            chapter_normalized[chapter] = {
                comp: round(count / total, 3) for comp, count in counts.items()
            }
        
        # Detect trends (is application increasing?)
        year_trends = {}
        sorted_years = sorted(year_competency.keys())
        if len(sorted_years) >= 2:
            for comp in COMPETENCY_PATTERNS.keys():
                values = []
                for year in sorted_years[-4:]:  # Last 4 years
                    year_total = sum(year_competency[year].values()) or 1
                    values.append(year_competency[year].get(comp, 0) / year_total)
                
                if len(values) >= 2:
                    trend = (values[-1] - values[0]) / len(values)
                    year_trends[comp] = round(trend, 4)
        
        trends[subject] = {
            "overall_distribution": dict(overall_competency),
            "chapter_competency": chapter_normalized,
            "year_trends": year_trends,
            "dominant_competency": overall_competency.most_common(1)[0][0] if overall_competency else "understanding",
        }
    
    return trends


def get_competency_signal(subjects: list[str], pdf_analysis: dict) -> dict[str, dict]:
    """Get competency-based signal for scoring.
    
    Chapters with increasing application/analysis competency demand
    are more likely to have complex questions in upcoming exams.
    """
    trends = analyze_competency_trends(pdf_analysis)
    
    signals = {}
    for subject in subjects:
        chapter_signals = {}
        subject_trends = trends.get(subject, {})
        chapter_comps = subject_trends.get("chapter_competency", {})
        year_trends = subject_trends.get("year_trends", {})
        
        # Application trend is key indicator
        app_trend = year_trends.get("application", 0)
        analysis_trend = year_trends.get("analysis", 0)
        
        for chapter in BLUEPRINT[subject]["chapters"]:
            if BLUEPRINT[subject]["chapters"][chapter].get("deleted"):
                continue
            
            comp_dist = chapter_comps.get(chapter, {})
            
            # Signal based on application/analysis weight in chapter
            app_weight = comp_dist.get("application", 0)
            analysis_weight = comp_dist.get("analysis", 0)
            
            # Higher signal for chapters with strong application component
            # that aligns with increasing trend
            signal = 0.5  # Base
            
            if app_weight > 0.3:
                signal += 0.2
            if analysis_weight > 0.2:
                signal += 0.15
            
            # Boost if application trend is increasing
            if app_trend > 0:
                signal += app_trend * 2
            
            chapter_signals[chapter] = round(min(1.0, max(0.0, signal)), 4)
        
        # Normalize
        if chapter_signals:
            max_sig = max(chapter_signals.values())
            if max_sig > 0:
                chapter_signals = {ch: round(s / max_sig, 4) for ch, s in chapter_signals.items()}
        
        signals[subject] = chapter_signals
    
    return signals


def get_competency_requirements(subject: str) -> dict[str, dict]:
    """Get expected competency distribution per chapter based on blueprint."""
    requirements = {}
    
    for chapter, data in BLUEPRINT[subject]["chapters"].items():
        if data.get("deleted"):
            continue
        
        # Use blueprint competency if available, else estimate
        comp = data.get("competency", {})
        if not comp:
            # Default based on chapter characteristics
            weight = data.get("weight", 5)
            if weight >= 7:
                comp = {"knowledge": 0.2, "understanding": 0.3, "application": 0.4, "analysis": 0.1}
            elif weight >= 4:
                comp = {"knowledge": 0.25, "understanding": 0.4, "application": 0.3, "analysis": 0.05}
            else:
                comp = {"knowledge": 0.35, "understanding": 0.45, "application": 0.2}
        
        requirements[chapter] = comp
    
    return requirements
