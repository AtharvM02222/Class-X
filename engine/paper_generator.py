"""engine/paper_generator.py — generates full mock papers with solutions."""
import json, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TEMP, GEMINI_MAX_TOKENS,
                    QUESTION_DISTRIBUTION, PAPER_TEMPLATES, TARGET_YEAR, OUTPUT_DIR)
from blueprint import BLUEPRINT
import google.generativeai as genai


PAPER_SYSTEM_PROMPT = """You are an expert CBSE Class 10 board exam paper setter with 20 years of experience.
You create authentic, exam-grade question papers that follow CBSE guidelines precisely.
Your papers match the exact format, difficulty distribution, and style of real board exams.
You are creating a paper for the {year} Board Examination."""


def _build_paper_prompt(subject: str, chapter_scores: dict, template: str = "full_paper",
                        include_solutions: bool = True) -> str:
    """Build the prompt for paper generation."""
    s_display = subject.replace("_", " ").title()
    template_config = PAPER_TEMPLATES.get(template, PAPER_TEMPLATES["full_paper"])
    
    # Get top chapters by score
    top_chapters = sorted(chapter_scores.items(), key=lambda x: -x[1]["score"])[:10]
    chapter_context = "\n".join([
        f"  • {ch}: Score {d['score']:.3f}, Confidence {d['confidence']}, Unit: {d['unit']}"
        for ch, d in top_chapters
    ])
    
    # Question type distribution
    qtypes = BLUEPRINT[subject].get("question_types", {})
    qtype_str = "\n".join([
        f"  Section {d.get('section', '?')}: {qt} - {d['marks']} marks × {d['count']} questions"
        for qt, d in qtypes.items()
    ])
    
    # Internal choice info
    internal_choice = BLUEPRINT[subject].get("internal_choice", {})
    choice_str = ", ".join([f"{k}: {v} questions" for k, v in internal_choice.items()])
    
    # Map work for SST
    map_info = ""
    if subject == "social_science":
        map_work = BLUEPRINT["social_science"].get("map_work", {})
        map_info = f"""
## MAP WORK (5 marks - guaranteed)
History locations: {', '.join(map_work.get('history', [])[:5])}
Geography locations: {', '.join(map_work.get('geography', [])[:5])}
"""

    solutions_instruction = """
13. For EACH question, provide:
    - The complete question text
    - Model answer with step-by-step working
    - Marking scheme breakdown (how marks are distributed)
    - Key points that must be included for full marks
""" if include_solutions else ""

    return f"""{PAPER_SYSTEM_PROMPT.format(year=TARGET_YEAR)}

SUBJECT: {s_display}
Paper Type: {template}
Duration: {template_config['duration']}
Maximum Marks: {template_config['total_marks']}

## TOP SCORING CHAPTERS (prioritize these)
{chapter_context}

## OFFICIAL QUESTION PAPER STRUCTURE
{qtype_str}

Internal choices available in: {choice_str or "None specified"}
{map_info}

## PAPER GENERATION RULES
1. Follow the exact section-wise structure shown above
2. Start with General Instructions (time, marks, sections, internal choice rules)
3. Section A: MCQs including 2 Assertion-Reason type
4. Include exactly 2 Case Study/Passage-based questions
5. Distribute questions across units proportionally to blueprint weights
6. Ensure variety: factual, conceptual, application, diagram-based, numerical
7. Questions must be original but CBSE-style (not copied from any textbook verbatim)
8. For Long Answer questions, always specify "OR" alternative questions
9. Include diagram requirements where appropriate (mark with [DIAGRAM])
10. For numericals, include realistic values that lead to clean answers
11. Map question (for SST) must have exactly 5 items to locate/mark
12. Difficulty distribution: 35% Easy, 45% Medium, 20% Hard
{solutions_instruction}

## OUTPUT FORMAT
Generate a complete, ready-to-print question paper in the following JSON format:

{{
  "metadata": {{
    "subject": "{s_display}",
    "class": "X",
    "year": {TARGET_YEAR},
    "duration": "{template_config['duration']}",
    "max_marks": {template_config['total_marks']},
    "generated_at": "ISO timestamp"
  }},
  "general_instructions": ["instruction1", "instruction2", ...],
  "sections": [
    {{
      "name": "Section A",
      "description": "Multiple Choice Questions",
      "questions": [
        {{
          "number": 1,
          "text": "Full question text",
          "options": {{"a": "...", "b": "...", "c": "...", "d": "..."}},
          "marks": 1,
          "chapter": "Chapter Name",
          "type": "MCQ",
          "difficulty": "Easy",
          "answer": "correct option letter",
          "explanation": "Why this is correct"
        }}
      ]
    }}
  ]
}}

Generate the complete paper now. Output ONLY valid JSON, no markdown fences or explanation."""


def generate_paper(subject: str, chapter_scores: dict, template: str = "full_paper",
                   include_solutions: bool = True) -> dict:
    """Generate a complete mock paper for a subject."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set")
    
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    prompt = _build_paper_prompt(subject, chapter_scores, template, include_solutions)
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=GEMINI_TEMP,
                max_output_tokens=GEMINI_MAX_TOKENS,
            ),
        )
        raw = response.text.strip()
        
        # Parse JSON
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]
        
        paper = json.loads(raw)
        paper["metadata"]["generated_at"] = datetime.now().isoformat()
        
        return paper
        
    except Exception as e:
        return {"error": str(e), "raw_response": response.text if 'response' in dir() else ""}


def save_paper(paper: dict, subject: str, template: str = "full_paper") -> Path:
    """Save generated paper to file."""
    filename = f"{subject}_{template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(paper, f, indent=2, ensure_ascii=False)
    
    return filepath


def paper_to_text(paper: dict) -> str:
    """Convert paper JSON to printable text format."""
    lines = []
    meta = paper.get("metadata", {})
    
    # Header
    lines.append("=" * 70)
    lines.append(f"CENTRAL BOARD OF SECONDARY EDUCATION")
    lines.append(f"CLASS X BOARD EXAMINATION {meta.get('year', TARGET_YEAR)}")
    lines.append(f"SUBJECT: {meta.get('subject', 'Unknown').upper()}")
    lines.append(f"Time: {meta.get('duration', '3 hours')}    Maximum Marks: {meta.get('max_marks', 80)}")
    lines.append("=" * 70)
    lines.append("")
    
    # General Instructions
    lines.append("GENERAL INSTRUCTIONS:")
    for i, inst in enumerate(paper.get("general_instructions", []), 1):
        lines.append(f"  {i}. {inst}")
    lines.append("")
    
    # Sections
    for section in paper.get("sections", []):
        lines.append("-" * 70)
        lines.append(f"{section.get('name', 'Section')}: {section.get('description', '')}")
        lines.append("-" * 70)
        
        for q in section.get("questions", []):
            lines.append(f"\nQ{q.get('number', '?')}. [{q.get('marks', '?')} marks] [{q.get('chapter', '')}]")
            lines.append(f"    {q.get('text', '')}")
            
            # Options for MCQ
            if q.get("options"):
                for opt, text in q["options"].items():
                    lines.append(f"    ({opt}) {text}")
            
            # Answer (if included)
            if q.get("answer"):
                lines.append(f"    Answer: {q['answer']}")
            if q.get("explanation"):
                lines.append(f"    Explanation: {q['explanation']}")
        
        lines.append("")
    
    return "\n".join(lines)


def paper_to_html(paper: dict) -> str:
    """Convert paper JSON to styled HTML for printing."""
    meta = paper.get("metadata", {})
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{meta.get('subject', 'Unknown')} - Class X Board Exam {meta.get('year', TARGET_YEAR)}</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        .header {{ text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 18px; }}
        .header h2 {{ margin: 5px 0; font-size: 16px; }}
        .instructions {{ background: #f5f5f5; padding: 15px; margin-bottom: 20px; border-left: 4px solid #333; }}
        .section {{ margin-bottom: 30px; }}
        .section-header {{ background: #333; color: white; padding: 10px; font-weight: bold; }}
        .question {{ margin: 15px 0; padding: 10px; border-bottom: 1px dashed #ccc; }}
        .question-num {{ font-weight: bold; color: #333; }}
        .marks {{ float: right; color: #666; font-size: 12px; }}
        .options {{ margin-left: 30px; }}
        .answer {{ background: #e8f5e9; padding: 10px; margin-top: 10px; border-left: 4px solid #4caf50; }}
        @media print {{ .answer {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CENTRAL BOARD OF SECONDARY EDUCATION</h1>
        <h2>CLASS X BOARD EXAMINATION {meta.get('year', TARGET_YEAR)}</h2>
        <h2>SUBJECT: {meta.get('subject', 'Unknown').upper()}</h2>
        <p>Time: {meta.get('duration', '3 hours')} | Maximum Marks: {meta.get('max_marks', 80)}</p>
    </div>
    
    <div class="instructions">
        <strong>GENERAL INSTRUCTIONS:</strong>
        <ol>
"""
    
    for inst in paper.get("general_instructions", []):
        html += f"            <li>{inst}</li>\n"
    
    html += """        </ol>
    </div>
"""
    
    for section in paper.get("sections", []):
        html += f"""
    <div class="section">
        <div class="section-header">{section.get('name', 'Section')}: {section.get('description', '')}</div>
"""
        
        for q in section.get("questions", []):
            html += f"""
        <div class="question">
            <span class="question-num">Q{q.get('number', '?')}.</span>
            <span class="marks">[{q.get('marks', '?')} marks | {q.get('chapter', '')}]</span>
            <p>{q.get('text', '')}</p>
"""
            
            if q.get("options"):
                html += '            <div class="options">\n'
                for opt, text in q["options"].items():
                    html += f"                ({opt}) {text}<br>\n"
                html += "            </div>\n"
            
            if q.get("answer"):
                html += f"""            <div class="answer">
                <strong>Answer:</strong> {q['answer']}<br>
                <strong>Explanation:</strong> {q.get('explanation', '')}
            </div>
"""
            
            html += "        </div>\n"
        
        html += "    </div>\n"
    
    html += """
</body>
</html>"""
    
    return html
