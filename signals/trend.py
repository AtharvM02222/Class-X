"""signals/trend.py — year-over-year trend, gap bonuses, alternation, unit saturation."""
import sys
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).parent.parent))
from blueprint import BLUEPRINT, HISTORY, LAST_SEEN

CURRENT = 2025
RECENCY = {2024:1.0,2023:0.85,2022:0.70,2020:0.55,2019:0.40,2018:0.30,2017:0.20,2016:0.10}

def gap_bonus(subject: str) -> dict[str, float]:
    """Chapters absent for N years get a proportional bonus — they're overdue."""
    bonuses = {}
    last_seen_map = LAST_SEEN.get(subject, {})
    history       = HISTORY.get(subject, {})
    for chapter in BLUEPRINT[subject]["chapters"]:
        last = last_seen_map.get(chapter)
        if not last:
            years = history.get(chapter, [])
            last  = max(years) if years else CURRENT - 6
        gap = CURRENT - last
        if   gap >= 4: bonuses[chapter] = 1.0
        elif gap == 3: bonuses[chapter] = 0.75
        elif gap == 2: bonuses[chapter] = 0.45
        elif gap == 1: bonuses[chapter] = 0.20
        else:          bonuses[chapter] = 0.0
    return bonuses

def frequency_score(subject: str) -> dict[str, float]:
    """Recency-weighted historical frequency — how reliably does this chapter appear?"""
    history = HISTORY.get(subject, {})
    scores  = {}
    for chapter in BLUEPRINT[subject]["chapters"]:
        years = history.get(chapter, [])
        score = sum(RECENCY.get(y, 0.05) for y in years)
        scores[chapter] = round(score, 4)
    mx = max(scores.values(), default=1)
    return {c: round(s/mx, 4) for c,s in scores.items()}

def alternation_signal(subject: str, year_data: dict) -> dict[str, float]:
    """If a chapter dominated LAST year's paper → slight penalty (rotation effect)."""
    if not year_data: return {c: 0.0 for c in BLUEPRINT[subject]["chapters"]}
    recent = sorted(year_data.keys(), reverse=True)[:1]
    hot_chapters = set()
    for y in recent:
        for ch, sc in year_data.get(y, {}).items():
            if sc > 8: hot_chapters.add(ch)
    return {c: (-0.12 if c in hot_chapters else 0.08) for c in BLUEPRINT[subject]["chapters"]}

def unit_balance(subject: str, chap_freq: dict) -> dict[str, float]:
    """If a unit is overrepresented in past papers, boost chapters from under-represented units."""
    units_data  = BLUEPRINT[subject].get("units", {})
    unit_scores: dict = defaultdict(float)
    for ch, sc in chap_freq.items():
        unit = BLUEPRINT[subject]["chapters"].get(ch, {}).get("unit","")
        unit_scores[unit] += sc
    if not unit_scores: return {c: 0.0 for c in BLUEPRINT[subject]["chapters"]}
    mx = max(unit_scores.values())
    unit_norm = {u: s/mx for u, s in unit_scores.items()}
    result = {}
    for ch, data in BLUEPRINT[subject]["chapters"].items():
        unit = data.get("unit", "")
        sat  = unit_norm.get(unit, 0.5)
        result[ch] = round((1.0 - sat) * 0.25, 4)   # inverse saturation bonus
    return result

def get_all_trend_signals(subjects: list[str], pdf_analysis: dict) -> dict[str, dict]:
    return {
        s: {
            "gap_bonus":    gap_bonus(s),
            "freq_score":   frequency_score(s),
            "alternation":  alternation_signal(s, pdf_analysis.get(s,{}).get("year_data",{})),
            "unit_balance": unit_balance(s, pdf_analysis.get(s,{}).get("chapter_freq",{})),
        }
        for s in subjects
    }
