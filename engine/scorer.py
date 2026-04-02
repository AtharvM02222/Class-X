"""engine/scorer.py — combines all signals into final per-chapter composite score."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import WEIGHTS, CONFIDENCE_BANDS
from blueprint import BLUEPRINT

def _norm(d: dict) -> dict:
    """Normalize dictionary values to [0, 1] range."""
    mx = max(d.values(), default=1) or 1
    return {k: round(v/mx, 4) for k, v in d.items()}

def _safe_get(d: dict, key: str, default: float = 0.0) -> float:
    """Safely get a value from a dict, handling None."""
    val = d.get(key)
    return float(val) if val is not None else default

def score_subject(subject: str, pdf: dict, yt: dict, trend: dict,
                  preboard: dict = None, blog: dict = None, 
                  difficulty: dict = None, examiner: dict = None,
                  competency: dict = None) -> dict[str, dict]:
    """Score all chapters in a subject using multiple signal sources."""
    chapters = [c for c, d in BLUEPRINT[subject]["chapters"].items() if not d.get("deleted")]
    bp_data = BLUEPRINT[subject]["chapters"]

    # Normalize all input signals
    bp_raw = {c: bp_data[c]["weight"] for c in chapters}
    bp_n = _norm(bp_raw)
    
    # Core signals
    pdf_freq = _norm(pdf.get("chapter_freq", {}))
    yt_scores = _norm(yt.get("chapter_scores", {}))
    yt_pred = _norm({
        c: sum(1 for v in yt.get("prediction_videos", []) if c in v.get("chapters", []))
        for c in chapters
    })
    ncert_n = _norm({
        c: bp_data[c].get("exemplar", 0) + bp_data[c].get("ncert_ex", 0) 
        for c in chapters
    })

    # Trend signals
    gap = trend.get("gap_bonus", {})
    freq = trend.get("freq_score", {})
    alt = trend.get("alternation", {})
    ubal = trend.get("unit_balance", {})

    # New signals (with defaults)
    preboard_sig = _norm(preboard) if preboard else {}
    blog_sig = _norm(blog) if blog else {}
    difficulty_sig = difficulty if difficulty else {}
    examiner_sig = examiner if examiner else {}
    competency_sig = competency if competency else {}

    W = WEIGHTS
    results = {}
    
    for ch in chapters:
        # Core signals
        bp = bp_n.get(ch, 0)
        pdf_val = pdf_freq.get(ch, 0)
        fq = freq.get(ch, 0)
        gp = gap.get(ch, 0)
        yt_val = yt_scores.get(ch, 0)
        yp = yt_pred.get(ch, 0)
        nc = ncert_n.get(ch, 0)
        ub = ubal.get(ch, 0)
        al = alt.get(ch, 0)

        # New signals
        pb = preboard_sig.get(ch, 0)
        bl = blog_sig.get(ch, 0)
        df = _safe_get(difficulty_sig, ch, 0.5)
        ex = _safe_get(examiner_sig, ch, 0.5)
        cp = _safe_get(competency_sig, ch, 0.5)

        # Weighted score calculation
        score = (
            bp * W["blueprint"] +
            pdf_val * W["pyq_frequency"] +
            fq * W["year_trend"] +
            gp * W["gap_bonus"] +
            yt_val * W["yt_mentions"] +
            yp * W["yt_prediction"] +
            nc * W["ncert_density"] +
            ub * W["unit_balance"] +
            pb * W.get("preboard_signal", 0) +
            bl * W.get("blog_consensus", 0) +
            df * W.get("difficulty_prog", 0) +
            ex * W.get("examiner_pref", 0) +
            cp * W.get("competency_map", 0) +
            al * 0.03  # Alternation adjustment
        )

        score = round(max(0.0, min(1.0, score)), 4)
        conf = next((label for label, thresh in CONFIDENCE_BANDS.items() if score >= thresh), "Low")

        results[ch] = {
            "score": score,
            "confidence": conf,
            "rank": 0,  # Filled below
            "unit": bp_data[ch].get("unit", ""),
            "key_topics": bp_data[ch].get("key_topics", []),
            "high_yield": bp_data[ch].get("high_yield", []),
            "components": {
                "blueprint": round(bp, 3),
                "past_papers": round(pdf_val, 3),
                "year_trend": round(fq, 3),
                "gap_bonus": round(gp, 3),
                "yt_signal": round(yt_val, 3),
                "yt_pred": round(yp, 3),
                "ncert": round(nc, 3),
                "unit_balance": round(ub, 3),
                "alternation_adj": round(al, 3),
                "preboard": round(pb, 3),
                "blog": round(bl, 3),
                "difficulty": round(df, 3),
                "examiner": round(ex, 3),
                "competency": round(cp, 3),
            },
        }

    # Rank chapters by score
    ranked = sorted(results.items(), key=lambda x: -x[1]["score"])
    for i, (ch, _) in enumerate(ranked, 1):
        results[ch]["rank"] = i
    
    return results


def score_all(subjects: list[str], pdf_analysis: dict, yt_all: dict, trend_all: dict,
              preboard_all: dict = None, blog_all: dict = None,
              difficulty_all: dict = None, examiner_all: dict = None,
              competency_all: dict = None) -> dict[str, dict]:
    """Score all subjects with all available signals."""
    results = {}
    
    for s in subjects:
        results[s] = score_subject(
            s,
            pdf_analysis.get(s, {}),
            yt_all.get(s, {}),
            trend_all.get(s, {}),
            preboard=preboard_all.get(s, {}) if preboard_all else None,
            blog=blog_all.get(s, {}) if blog_all else None,
            difficulty=difficulty_all.get(s, {}) if difficulty_all else None,
            examiner=examiner_all.get(s, {}) if examiner_all else None,
            competency=competency_all.get(s, {}) if competency_all else None,
        )
    
    return results


def get_top_chapters(subject: str, chapter_scores: dict, n: int = 10) -> list[tuple[str, dict]]:
    """Get top N chapters by score for a subject."""
    return sorted(chapter_scores.items(), key=lambda x: -x[1]["score"])[:n]


def get_high_gap_chapters(subject: str, trend: dict, threshold: float = 0.5) -> list[str]:
    """Get chapters with high gap bonus (overdue)."""
    gap_bonus = trend.get("gap_bonus", {})
    return [ch for ch, bonus in gap_bonus.items() if bonus >= threshold]


def get_signal_summary(chapter_scores: dict) -> dict:
    """Get a summary of signal contributions across all chapters."""
    summary = {
        "avg_score": 0,
        "high_confidence_count": 0,
        "medium_confidence_count": 0,
        "low_confidence_count": 0,
        "top_signal_contributors": {},
    }
    
    if not chapter_scores:
        return summary
    
    scores = [d["score"] for d in chapter_scores.values()]
    summary["avg_score"] = round(sum(scores) / len(scores), 3)
    
    for data in chapter_scores.values():
        conf = data.get("confidence", "Low")
        if conf == "High":
            summary["high_confidence_count"] += 1
        elif conf == "Medium":
            summary["medium_confidence_count"] += 1
        else:
            summary["low_confidence_count"] += 1
    
    # Find which signals contribute most
    signal_totals = {}
    for data in chapter_scores.values():
        for signal, value in data.get("components", {}).items():
            signal_totals[signal] = signal_totals.get(signal, 0) + value
    
    summary["top_signal_contributors"] = dict(
        sorted(signal_totals.items(), key=lambda x: -x[1])[:5]
    )
    
    return summary
