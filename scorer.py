"""engine/scorer.py — combines all signals into final per-chapter composite score."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import WEIGHTS, CONFIDENCE_BANDS
from blueprint import BLUEPRINT

def _norm(d: dict) -> dict:
    mx = max(d.values(), default=1) or 1
    return {k: round(v/mx, 4) for k,v in d.items()}

def score_subject(subject: str, pdf: dict, yt: dict, trend: dict) -> dict[str, dict]:
    chapters  = [c for c,d in BLUEPRINT[subject]["chapters"].items() if not d.get("deleted")]
    bp_data   = BLUEPRINT[subject]["chapters"]

    bp_raw    = {c: bp_data[c]["weight"] for c in chapters}
    bp_n      = _norm(bp_raw)
    pdf_freq  = _norm(pdf.get("chapter_freq", {}))
    yt_scores = _norm(yt.get("chapter_scores", {}))
    yt_pred   = _norm({c: sum(1 for v in yt.get("prediction_videos",[]) if c in v.get("chapters",[])) for c in chapters})
    ncert_n   = _norm({c: bp_data[c].get("exemplar",0) + bp_data[c].get("ncert_ex",0) for c in chapters})

    gap   = trend.get("gap_bonus",    {})
    freq  = trend.get("freq_score",   {})
    alt   = trend.get("alternation",  {})
    ubal  = trend.get("unit_balance", {})

    W = WEIGHTS
    results = {}
    for ch in chapters:
        bp  = bp_n.get(ch,0)
        pdf = pdf_freq.get(ch,0)
        fq  = freq.get(ch,0)
        gp  = gap.get(ch,0)
        yt  = yt_scores.get(ch,0)
        yp  = yt_pred.get(ch,0)
        nc  = ncert_n.get(ch,0)
        ub  = ubal.get(ch,0)
        al  = alt.get(ch,0)

        score = (bp  * W["blueprint"]      +
                 pdf * W["pyq_frequency"]  +
                 fq  * W["year_trend"]     +
                 gp  * W["gap_bonus"]      +
                 yt  * W["yt_mentions"]    +
                 yp  * W["yt_prediction"]  +
                 nc  * W["ncert_density"]  +
                 ub  * W["unit_balance"]   +
                 al  * 0.04)

        score = round(max(0.0, min(1.0, score)), 4)
        conf  = next((label for label,thresh in CONFIDENCE_BANDS.items() if score >= thresh), "Low")

        results[ch] = {
            "score":      score,
            "confidence": conf,
            "rank":       0,   # filled below
            "unit":       bp_data[ch].get("unit",""),
            "key_topics": bp_data[ch].get("key_topics",[]),
            "breakdown": {
                "blueprint":    round(bp,3),
                "pyq_freq":     round(pdf_freq.get(ch,0),3),
                "year_trend":   round(fq,3),
                "gap_bonus":    round(gp,3),
                "yt_signal":    round(yt,3),
                "yt_pred":      round(yp,3),
                "ncert":        round(nc,3),
                "unit_balance": round(ub,3),
                "alternation":  round(al,3),
            },
        }

    ranked = sorted(results.items(), key=lambda x: -x[1]["score"])
    for i, (ch,_) in enumerate(ranked,1): results[ch]["rank"] = i
    return results

def score_all(subjects, pdf_analysis, yt_all, trend_all):
    return {s: score_subject(s, pdf_analysis.get(s,{}), yt_all.get(s,{}), trend_all.get(s,{})) for s in subjects}
