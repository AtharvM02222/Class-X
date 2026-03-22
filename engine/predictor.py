"""engine/predictor.py — Gemini-powered question generation with full context."""
import json, sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TEMP, GEMINI_MAX_TOKENS, QUESTION_DISTRIBUTION
from blueprint import BLUEPRINT
import google.generativeai as genai

# ── Expert Intelligence (from IMP.md) ─────────────────────────────────────────
SUBJECT_INTELLIGENCE = {
    "science": """
### Science-Specific Intelligence (2026 Target)
- **Life Processes** (10-weight, 8/8 years): SA-II or LA every year. Photosynthesis formula, excretion (nephron diagram), blood circulation diagram are safe bets.
- **Light — Reflection & Refraction** (7-weight, 8/8 years): Mirror/lens formula numericals, ray diagrams with object positions, power of lens. Mirror formula + ray diagram is a near-certain LA.
- **Electricity** (7-weight, 8/8 years): Ohm's law derivation, series/parallel resistance, Joule's heating numerical, domestic wiring. Always numerical LA.
- **Chemical Reactions** (7-weight, 8/8 years): Balancing equations (always MCQ + SA), types of reactions, corrosion/rancidity.
- **Acids, Bases and Salts** (8-weight, highest blueprint weight): pH, neutralisation, baking soda vs washing soda distinction, bleaching powder. High-value SA-II or LA.
- **Carbon and Its Compounds** (gap: last seen 2023): Homologous series, IUPAC nomenclature, ethanol vs ethanoic acid, soaps/detergents mechanism. Due for LA in 2026.
- **Heredity** (gap: 2023 only recent): Mendel's laws, monohybrid/dihybrid cross diagram, sex determination. High gap bonus.
- **Diagrams**: Ray diagrams (Light), circuit diagrams (Electricity), reflex arc (Control), nephron/heart (Life Processes) are perennial.
""",
    "math": """
### Mathematics-Specific Intelligence (2026 Target)
- **Real Numbers**: HCF/LCM by Euclid's algorithm is MCQ every year. Irrationality proofs appear in SA.
- **Quadratic Equations**: Discriminant nature-of-roots is guaranteed MCQ. Word problems (speed/time, dimensions) appear as LA.
- **Arithmetic Progressions**: nth term + sum of n terms word problems are SA-II/LA staples.
- **Triangles**: BPT/Thales theorem proof is the single most-asked LA in CBSE Maths history. Include it.
- **Trigonometry**: Identity-based simplifications appear every year. Heights & Distances word problems (2 buildings, tower/river) are guaranteed SA-II or LA.
- **Statistics**: Mean by step-deviation method, median from ogive, mode — all three types appear in one question or separately.
- **Circles**: Tangent-length from external point + proof of tangent perpendicular to radius — near-certain.
- **Areas Related to Circles** (gap: last seen 2023): Sector/segment area combination figures — overdue.
""",
    "social_science": """
### Social Science-Specific Intelligence (2026 Target)
- **Nationalism in India** (8-weight, 8/8 years): Non-Cooperation Movement, Civil Disobedience, Rowlatt Act, Gandhi's role — guaranteed SA-II or LA.
- **Power Sharing** (5-weight, 8/8 years): Belgium vs Sri Lanka case, forms of power sharing, coalition — reliable SA or LA.
- **Development** (5-weight, 8/8 years): Per capita income vs HDI, Kerala-Punjab comparison, sustainable development — always present.
- **Federalism** (5-weight, 7/8 years): Decentralisation, panchayati raj, coming together vs holding together — SA or LA.
- **The Rise of Nationalism in Europe** (7/8 years): Massini/Garibaldi, German/Italian unification, Zollverein, allegorical figures — frequent SA-II.
- **Sectors of Indian Economy**: Primary/secondary/tertiary, GDP, NREGA, organised vs unorganised — LA candidate.
- **Map Work** (100% guarantee — 5 marks):
  - History: Peasant movements (Champaran, Kheda, Bardoli), Salt March route, Pre-independence industrial locations
  - Geography: Multipurpose dams (Bhakra-Nangal, Hirakud, Tehri), Iron & Steel plants (TISCO Jamshedpur, Bhilai, Bokaro), Major ports (Mumbai, Chennai, Visakhapatnam, Kolkata)
"""
}

SYSTEM_CONTEXT = """You are an elite CBSE Class 10 exam analyst with 15 years of experience.
You have studied every board paper since 2010, all CBSE circulars, NCERT revisions, and
topper answer scripts. Your predictions are data-driven and specific. You generate questions
in the exact style of CBSE — not textbook copy-paste, but real exam-grade original questions.
You are predicting for the 2026 Board Exam (Session 2025-26)."""

def _build_chapter_context(subject: str, chapter_scores: dict) -> str:
    top = sorted(chapter_scores.items(), key=lambda x: -x[1]["score"])[:14]
    lines = []
    for chap, data in top:
        comps = data["components"]
        lines.append(
            f"  • {chap} | Score:{data['score']:.3f} | Conf:{data['confidence']} | "
            f"BP:{comps['blueprint']:.2f} PDF:{comps['past_papers']:.2f} "
            f"YT:{comps['yt_signal']:.2f} Gap:{comps['gap_bonus']:.2f} "
            f"Alt:{comps['alternation_adj']:.2f} Rank:#{data['rank']}"
        )
    return "\n".join(lines)

def _question_type_guide(subject: str) -> str:
    qtype = BLUEPRINT[subject].get("question_types", {})
    lines = []
    for qt, d in qtype.items():
        lines.append(f"  {qt}: {d['marks']} marks x {d['count']} questions = {d['marks']*d['count']} marks")
    ic = BLUEPRINT[subject].get("internal_choice_sections", {})
    if ic:
        lines.append(f"  Internal choices in: {', '.join(f'{k}({v})' for k,v in ic.items())}")
    return "\n".join(lines)

def _format_pdf_questions(questions: list[dict]) -> str:
    if not questions:
        return "  (no PDF data available — rely on blueprint + trend signals)"
    lines = []
    for q in questions[:10]:
        lines.append(f"  [{q.get('type','?')}|{q.get('year','?')}|{q.get('chapter','?')[:25]}] {q['q'][:130]}")
    return "\n".join(lines)

def _format_yt_videos(videos: list[dict]) -> str:
    if not videos:
        return "  (no YouTube data — rely on blueprint + paper signals)"
    lines = []
    for v in videos[:8]:
        chaps = ", ".join(v.get("chapters", [])[:3])
        lines.append(f"  [{v['channel']} | score:{v['score']:.2f}] {v['title'][:70]}")
        if chaps:
            lines.append(f"    Chapters detected: {chaps}")
    return "\n".join(lines)

def _build_master_prompt(subject: str, chapter_scores: dict, pdf_questions: list,
                          yt_pred_videos: list, unit_saturation: dict, gap_bonus: dict, n: int) -> str:
    s_display   = subject.replace("_", " ").title()
    chap_ctx    = _build_chapter_context(subject, chapter_scores)
    qtype_guide = _question_type_guide(subject)
    pdf_ctx     = _format_pdf_questions(pdf_questions)
    yt_ctx      = _format_yt_videos(yt_pred_videos)
    subject_intel = SUBJECT_INTELLIGENCE.get(subject, "")

    top_gap = sorted([(c, v) for c, v in gap_bonus.items() if v > 0.4], key=lambda x: -x[1])
    gap_str = ", ".join(f"{c} (gap:{v:.1f})" for c, v in top_gap[:5]) or "none"

    map_hint = ""
    if subject == "social_science":
        mw = BLUEPRINT["social_science"].get("map_work", {})
        map_hint = (f"\n## MAP WORK (guaranteed 5 marks)\n"
                    f"History items: {mw.get('history',[])}.\n"
                    f"Geography items: {mw.get('geography',[])}.")

    dist = QUESTION_DISTRIBUTION.get(subject, {})
    dist_str = " | ".join(f"{m}M x{c}q" for m, c in sorted(dist.items()))

    return f"""{SYSTEM_CONTEXT}

SUBJECT: {s_display}  |  CBSE Class 10 Board Exam 2026 (Session 2025-26)

## HIGH-PROBABILITY INTELLIGENCE (Apply these patterns)
{subject_intel}

## COMPOSITE SIGNAL SCORES (multi-source AI analysis)
{chap_ctx}

## OVERDUE CHAPTERS (high probability due to absence gap)
{gap_str}

## OFFICIAL QUESTION PAPER STRUCTURE
{qtype_guide}
Target distribution: {dist_str}

## REAL QUESTIONS FROM PAST CBSE PAPERS (style reference)
{pdf_ctx}

## TOP PREDICTION VIDEOS BY CBSE YOUTUBERS
(Shobhit Nirwan, Prashant Kirad, Digraj Singh Rajput, Next Toppers)
{yt_ctx}
{map_hint}

## STRICT GENERATION RULES
1. Generate exactly {n} questions total.
2. Follow official marks distribution strictly ({dist_str}).
3. Prioritise High-confidence chapters (top scores), then gap-overdue ones.
4. Questions must be CBSE-style — application-based, specific, not vague.
5. Mix question types: factual, application, diagram, case-study, numerical.
6. Each LA (Long Answer) question must include a full "scheme" with marking value points.
7. Include at least 2 Assertion-Reason type MCQs (for Science/Math).
8. Include at least 2 Case-Study paragraph-based questions.
9. For Social Science: include exactly 1 Map question (5 marks).
10. No two questions from the same chapter+type combo unless blueprint demands it.
11. Phrase questions exactly as they would appear on the real board paper.
12. Populate "source_signals" with list of signals driving the prediction (e.g. "Blueprint", "YT:Shobhit", "GapBonus").

## OUTPUT FORMAT — ONLY raw JSON array, no markdown, no explanation:
IMPORTANT: Ensure the JSON is valid. Use escaped newlines (\\n) for any multi-line strings.
[
  {{
    "rank": 1,
    "question": "Full question text...",
    "chapter": "Chapter Name",
    "unit": "Unit Name",
    "marks": 5,
    "type": "LA",
    "confidence": "High",
    "scheme": "Marking scheme...",
    "source_signals": ["Signal1", "Signal2"],
    "reason": "Why this question?",
    "composite_score": 0.887
  }}
]"""

def _parse_response(raw: str) -> list[dict]:
    raw = raw.strip()
    # Find the outermost brackets
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end != -1:
        raw = raw[start:end+1]
    
    # Try direct parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: Try to fix common LLM mistakes (missing commas between objects)
        # Regex to find end of object '}' and start of next '{' without a comma
        fixed = re.sub(r'}\s*{', '}, {', raw)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError as e:
            # Last resort: try to extract objects one by one
            objs = []
            for m in re.finditer(r'\{.*?\}', raw, re.DOTALL):
                try:
                    objs.append(json.loads(m.group()))
                except:
                    pass
            if objs: return objs
            raise e

def generate_predictions(subjects: list[str], chapter_scores_all: dict,
                          pdf_analysis_all: dict, yt_all: dict,
                          trend_all: dict, num_questions: int = 25) -> dict[str, list[dict]]:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set.")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    results = {}

    for subject in subjects:
        print(f"  [gemini] {subject} ({num_questions}q)...", end=" ", flush=True)

        prompt = _build_master_prompt(
            subject        = subject,
            chapter_scores = chapter_scores_all.get(subject, {}),
            pdf_questions  = pdf_analysis_all.get(subject, {}).get("questions", []),
            yt_pred_videos = yt_all.get(subject, {}).get("prediction_videos", []),
            unit_saturation= trend_all.get(subject, {}).get("unit_saturation", {}),
            gap_bonus      = trend_all.get(subject, {}).get("gap_bonus", {}),
            n              = num_questions,
        )

        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature       = GEMINI_TEMP,
                    max_output_tokens = GEMINI_MAX_TOKENS,
                ),
            )
            raw       = response.text.strip()
            questions = _parse_response(raw)

            chapter_scores = chapter_scores_all.get(subject, {})
            for i, q in enumerate(questions, 1):
                q.setdefault("rank", i)
                q.setdefault("confidence", "Medium")
                q.setdefault("scheme", "")
                q.setdefault("source_signals", [])
                q.setdefault("type", "?")
                ch_name = q.get("chapter", "")
                ch_data = chapter_scores.get(ch_name, {})
                q["composite_score"] = round(ch_data.get("score", 0.0), 3)

            results[subject] = questions
            print(f"OK — {len(questions)} questions")

        except Exception as e:
            print(f"FAIL: {e}")
            results[subject] = []

    return results
