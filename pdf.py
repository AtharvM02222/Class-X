"""analyzers/pdf.py — deep PDF analysis: question extraction, chapter scoring, type tagging, year data."""
import re, sys
from collections import Counter, defaultdict
from pathlib import Path
import pdfplumber
sys.path.insert(0, str(Path(__file__).parent.parent))
from blueprint import BLUEPRINT

STOPW = {"and","the","of","in","a","an","its","how","do","with","for","to","is","are","was","were",
         "by","from","on","at","what","which","why","when","explain","describe","define","list",
         "state","give","draw","name","write","find","calculate","prove","show","compare",
         "differentiate","between","using","following","suitable","example","examples",
         "given","below","above","hence","therefore","thus","also","can","may","will","not","no"}

Q_RE     = re.compile(r"^(Q\.?\s*\d+[a-z]?|[a-d]\)|[ivx]+[\).]|\d+[\).])\s+.{10,}", re.I)
MARKS_RE = re.compile(r"\[(\d)\s*m\]|\((\d)\s*m(?:arks?)?\)|(\d)\s*×\s*\d|\((\d)\)", re.I)
MCQ_RE   = re.compile(r"\(a\).{1,60}\(b\).{1,60}\(c\).{1,60}\(d\)", re.I | re.S)
CASE_RE  = re.compile(r"(read the following|given passage|case study|given below|the above figure|refer to|the following table)", re.I)
DIAG_RE  = re.compile(r"(draw a (labelled )?diagram|label the|circuit diagram|ray diagram|draw and label)", re.I)
YEAR_RE  = re.compile(r"20([12]\d)")

def _extract_text(path: Path) -> list[str]:
    pages = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text(x_tolerance=3, y_tolerance=3)
                if t and len(t.strip()) > 50: pages.append(t)
    except Exception as e:
        print(f"warn: {path.name}: {e}")
    return pages

def _detect_year(filename: str) -> int:
    m = YEAR_RE.search(filename)
    return int("20" + m.group(1)) if m else 0

def _classify_qtype(text: str) -> str:
    m = MARKS_RE.search(text)
    marks = int(next((g for g in m.groups() if g), 0)) if m else 0
    if MCQ_RE.search(text) or marks == 1: return "MCQ"
    if CASE_RE.search(text):              return "CASE"
    if DIAG_RE.search(text):              return "DIAGRAM"
    if marks in (4,5):                    return "LA"
    if marks == 3:                        return "SA2"
    if marks == 2:                        return "SA1"
    return "OTHER"

def _chapter_score(text: str, chapter: str, subject: str) -> int:
    tl   = text.lower()
    data = BLUEPRINT[subject]["chapters"].get(chapter, {})
    kws  = [w for w in chapter.lower().split() if w not in STOPW and len(w)>3][:6]
    base = sum(tl.count(kw) for kw in kws)
    topic_hits  = sum(1 for t in data.get("key_topics",[]) if t.lower() in tl)
    specificity = sum(3 for kw in kws if len(kw)>7 and tl.count(kw)>0)
    return base + topic_hits * 3 + specificity

def analyze_pdfs(paths: list[Path], subject: str) -> dict:
    chapters  = [c for c,d in BLUEPRINT[subject]["chapters"].items() if not d.get("deleted")]
    chap_freq: Counter = Counter()
    type_cnt:  Counter = Counter()
    year_data: dict    = defaultdict(lambda: defaultdict(int))
    questions: list    = []

    for path in paths:
        year = _detect_year(path.name)
        print(f"  [pdf] {path.name[:50]} y={year or '?'}", end=" ", flush=True)
        pages = _extract_text(path)
        if not pages: print("— empty"); continue
        full = "\n".join(pages)

        for chapter in chapters:
            sc = _chapter_score(full, chapter, subject)
            chap_freq[chapter] += sc
            if year: year_data[year][chapter] += sc

        q_found = 0
        for page_text in pages:
            for line in page_text.split("\n"):
                line = line.strip()
                if len(line) < 25: continue
                if Q_RE.match(line):
                    qt = _classify_qtype(line)
                    type_cnt[qt] += 1
                    for chapter in chapters:
                        kws = [w for w in chapter.lower().split() if w not in STOPW and len(w)>3][:4]
                        if sum(1 for kw in kws if kw in line.lower()) >= min(2,len(kws)):
                            questions.append({"q":line[:220],"chapter":chapter,"type":qt,"year":year,"source":path.name})
                            q_found += 1; break
        print(f"— {q_found}q")

    return {
        "chapter_freq": dict(chap_freq.most_common()),
        "type_counts":  dict(type_cnt),
        "year_data":    {y:dict(d) for y,d in year_data.items()},
        "questions":    questions[:400],
        "total_papers": len(paths),
    }

def analyze_all(papers: dict[str, list[Path]]) -> dict[str, dict]:
    return {s: analyze_pdfs(paths, s) for s, paths in papers.items()}
