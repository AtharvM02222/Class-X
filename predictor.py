"""engine/predictor.py — Gemini-powered question generation with full context."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TEMP, GEMINI_MAX_TOKENS, QUESTION_DISTRIBUTION
from blueprint import BLUEPRINT
import google.generativeai as genai

SYSTEM_CONTEXT = """You are an elite CBSE Class 10 exam analyst with 15 years of experience.
You have studied every board paper since 2010, all CBSE circulars, NCERT revisions, and
topper answer scripts. Your predictions are data-driven and specific. You generate questions
in the exact style of CBSE — not textbook copy-paste, but real exam-grade original questions."""

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
        lines.append(f"  [{v['channel']} | score:{v['pred_score']:.2f}] {v['title'][:70]}")
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

SUBJECT: {s_display}  |  CBSE Class 10 Board Exam 2025

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
(Shobhit Nirwan, Prashant Dhawan, Digraj Singh Rajput, PW, CBSEWallah)
{yt_ctx}
{map_hint}

## STRICT GENERATION RULES
1. Generate exactly {n} questions total
2. Follow official marks distribution strictly
3. Prioritise High-confidence chapters, then gap-overdue ones
4. Questions must be CBSE-style — application-based, specific, not vague
5. Mix question types: factual, application, diagram, case-study, numerical
6. Each LA question must include a full "scheme" with marking value points
7. Include at least 2 Assertion-Reason type MCQs
8. Include at least 2 case-study paragraph-based questions
9. No two questions from the same chapter+type combo unless unavoidable
10. For Social Science: include exactly 1 map question (5 marks)
11. Phrase questions exactly as they would appear on the real board paper

## OUTPUT FORMAT — ONLY raw JSON array, no markdown, no explanation:
[
  {{
    "rank": 1,
    "question": "Full question text exactly as it would appear on the paper.",
    "chapter": "Exact chapter name matching blueprint",
    "unit": "Unit name",
    "marks": 3,
    "type": "SA-II",
    "confidence": "High",
    "scheme": "Key answer points: 1) ... 2) ... 3) ...",
    "source_signals": ["Blueprint:0.92","PastPapers:0.88","YT:Shobhit_Nirwan"],
    "reason": "appeared 7/8 years, gap_bonus=0.9, mentioned by Shobhit Nirwan in 3 videos"
  }}
]"""

def _parse_response(raw: str) -> list[dict]:
    raw = raw.strip()
    for fence in ["```json", "```JSON", "```"]:
        if fence in raw:
            raw = raw.split(fence, 1)[-1]
            raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()
    bracket_end = raw.rfind("]")
    if bracket_end != -1:
        raw = raw[:bracket_end+1]
    return json.loads(raw)

def generate_predictions(subjects: list[str], chapter_scores_all: dict,
                          pdf_analysis_all: dict, yt_all: dict,
                          trend_all: dict, num_questions: int = 25) -> dict[str, list[dict]]:
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY not set.\n"
            "Run: export GEMINI_API_KEY=your_key_here\n"
            "Get free key: https://aistudio.google.com/app/apikey"
        )

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
                ch_data = chapter_scores.get(q.get("chapter", ""), {})
                q["composite_score"] = round(ch_data.get("score", 0.0), 3)

            results[subject] = questions
            print(f"OK — {len(questions)} questions")

        except json.JSONDecodeError as e:
            print(f"FAIL (JSON): {e}")
            results[subject] = []
        except Exception as e:
            print(f"FAIL: {e}")
            results[subject] = []

    return results
