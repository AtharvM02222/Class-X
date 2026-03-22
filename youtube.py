"""scrapers/youtube.py — yt-dlp scraper for all 4 prediction channels with deep signal extraction."""
import json, re, sys
from pathlib import Path
from collections import Counter, defaultdict
import yt_dlp
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import YT_CHANNELS, YT_MAX_VIDEOS, YT_KEYWORDS, SUBJECT_CODES, CACHE_DIR

def _cache_path(name: str) -> Path:
    return CACHE_DIR / f"yt_{name}.json"

def _fetch_channel(name: str, url: str, force: bool = False) -> list[dict]:
    cp = _cache_path(name)
    if cp.exists() and not force:
        try: return json.loads(cp.read_text())
        except: pass
    opts = {"extract_flat":"in_playlist","quiet":True,"no_warnings":True,
            "playlistend":YT_MAX_VIDEOS,"ignoreerrors":True,"socket_timeout":30}
    entries = []
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info and "entries" in info:
                for e in (info["entries"] or []):
                    if e:
                        entries.append({"id":e.get("id",""),"title":e.get("title","") or "",
                                        "description":e.get("description","") or "",
                                        "view_count":e.get("view_count",0) or 0,
                                        "upload_date":e.get("upload_date","") or "","channel":name})
    except Exception as e:
        print(f"  [yt] {name} ERROR: {e}")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps(entries, indent=2))
    return entries

def _prediction_score(title: str, desc: str) -> float:
    text = (title + " " + desc).lower()
    hits = sum(1 for kw in YT_KEYWORDS if kw in text)
    year_bonus  = 0.25 if "2025" in text else 0.0
    title_bonus = 0.20 if any(kw in title.lower() for kw in YT_KEYWORDS) else 0.0
    return min(1.0, round((hits / 4) * 0.5 + year_bonus + title_bonus, 3))

def _recency_weight(upload_date: str) -> float:
    if not upload_date: return 0.5
    year = int(upload_date[:4]) if upload_date[:4].isdigit() else 2022
    return {2025:1.0,2024:0.85,2023:0.6,2022:0.4}.get(year, 0.25)

def _view_weight(views: int) -> float:
    if views >= 1_000_000: return 2.0
    if views >= 500_000:   return 1.6
    if views >= 100_000:   return 1.3
    if views >= 50_000:    return 1.1
    return 0.9

def _extract_chapters(text: str, subject: str) -> list[tuple[str, float]]:
    from blueprint import BLUEPRINT
    tl = text.lower()
    found = []
    stopw = {"and","the","of","in","a","an","its","how","do","with","for","to","is"}
    for chapter, data in BLUEPRINT[subject]["chapters"].items():
        if data.get("deleted"): continue
        words = [w for w in chapter.lower().split() if w not in stopw and len(w)>3][:5]
        hits  = sum(1 for w in words if w in tl)
        conf  = hits / max(len(words),1)
        topic_hits = sum(1 for t in data.get("key_topics",[]) if t.lower() in tl)
        total = min(1.0, conf + min(0.3, topic_hits*0.1))
        if total >= 0.35: found.append((chapter, round(total,3)))
    return found

def _is_subject(text: str, subject: str) -> bool:
    return any(c in text.lower() for c in SUBJECT_CODES[subject])

def scrape_youtube(subjects: list[str], force: bool = False) -> dict[str, dict]:
    all_videos: list[dict] = []
    for name, url in YT_CHANNELS.items():
        print(f"  [yt] {name}...", end=" ", flush=True)
        vids = _fetch_channel(name, url, force=force)
        all_videos.extend(vids)
        print(f"{len(vids)} videos")

    result = {s:{"chapter_scores":Counter(),"prediction_videos":[],"channel_breakdown":defaultdict(Counter),"total_pred_videos":0} for s in subjects}

    for vid in all_videos:
        full   = vid["title"] + " " + vid["description"]
        pscore = _prediction_score(vid["title"], vid["description"])
        rw     = _recency_weight(vid["upload_date"])
        vw     = _view_weight(vid["view_count"])
        weight = pscore * rw * vw

        for subject in subjects:
            if not _is_subject(full, subject): continue
            chapters = _extract_chapters(full, subject)
            for chapter, conf in chapters:
                w = conf * weight
                result[subject]["chapter_scores"][chapter] += w
                result[subject]["channel_breakdown"][vid["channel"]][chapter] += w
            if pscore >= 0.3 and chapters:
                result[subject]["prediction_videos"].append({
                    "title":vid["title"],"channel":vid["channel"],"score":pscore,
                    "views":vid["view_count"],"date":vid["upload_date"],
                    "chapters":[c for c,_ in chapters]})
                result[subject]["total_pred_videos"] += 1

    for s in subjects:
        result[s]["chapter_scores"]    = dict(result[s]["chapter_scores"].most_common(25))
        result[s]["channel_breakdown"] = {k:dict(v.most_common(8)) for k,v in result[s]["channel_breakdown"].items()}
        result[s]["prediction_videos"] = sorted(result[s]["prediction_videos"],key=lambda x:(-x["score"],-x.get("views",0)))[:40]
    return result
