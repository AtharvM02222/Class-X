"""scrapers/education_blogs.py — scrapes education blogs for prediction signals."""
import json, re, sys
from pathlib import Path
from collections import Counter, defaultdict
from urllib.parse import urljoin
from bs4 import BeautifulSoup
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import EDUCATION_BLOGS, CACHE_DIR, SUBJECT_CODES, TARGET_YEAR
from scrapers.http import fetch_text

def _cache_path(name: str) -> Path:
    return CACHE_DIR / f"blog_{name}.json"

def _extract_predictions(html: str, subject: str) -> dict:
    """Extract chapter predictions and important topics from blog HTML."""
    from blueprint import BLUEPRINT
    
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()
    
    chapter_scores = Counter()
    important_topics = []
    
    # Keywords that indicate prediction/importance
    prediction_keywords = [
        "important", "most expected", "sure shot", "must do", "high weightage",
        "frequently asked", "expected questions", "important questions",
        "board exam", str(TARGET_YEAR), str(TARGET_YEAR - 1),
    ]
    
    for chapter, data in BLUEPRINT[subject]["chapters"].items():
        if data.get("deleted"):
            continue
        
        # Score based on chapter name mentions
        chapter_lower = chapter.lower()
        base_score = text.count(chapter_lower)
        
        # Bonus for key topics mentioned
        topic_hits = sum(1 for t in data.get("key_topics", []) if t.lower() in text)
        
        # Bonus if mentioned near prediction keywords
        keyword_bonus = 0
        for kw in prediction_keywords:
            if kw in text:
                # Check if chapter is mentioned near this keyword
                pattern = rf"{re.escape(kw)}.{{0,200}}{re.escape(chapter_lower)}"
                if re.search(pattern, text):
                    keyword_bonus += 2
                pattern = rf"{re.escape(chapter_lower)}.{{0,200}}{re.escape(kw)}"
                if re.search(pattern, text):
                    keyword_bonus += 2
        
        total_score = base_score + topic_hits * 2 + keyword_bonus
        if total_score > 0:
            chapter_scores[chapter] = total_score
    
    # Extract specific important topics mentioned
    important_patterns = [
        r"important topics?:?\s*([^.]+)",
        r"must (do|prepare):?\s*([^.]+)",
        r"expected questions?:?\s*([^.]+)",
    ]
    for pattern in important_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                match = match[-1]
            important_topics.append(match[:200])
    
    return {
        "chapter_scores": dict(chapter_scores.most_common(15)),
        "important_topics": important_topics[:20],
    }

def _scrape_blog(name: str, url: str, subject: str, force: bool = False) -> dict:
    """Scrape a single blog for subject predictions."""
    cp = _cache_path(f"{name}_{subject}")
    if cp.exists() and not force:
        try:
            return json.loads(cp.read_text())
        except:
            pass
    
    result = {"chapter_scores": {}, "important_topics": [], "source": name}
    
    # Try to fetch the blog
    html = fetch_text(url)
    if not html:
        return result
    
    # Extract predictions
    predictions = _extract_predictions(html, subject)
    result.update(predictions)
    
    # Also try to find and follow "important questions" links
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        link_text = a.get_text(" ", strip=True).lower()
        href = a["href"]
        
        # Look for important questions pages
        if any(kw in link_text for kw in ["important", "expected", "prediction"]):
            if any(code in link_text or code in href.lower() for code in SUBJECT_CODES[subject]):
                sub_url = urljoin(url, href)
                sub_html = fetch_text(sub_url)
                if sub_html:
                    sub_pred = _extract_predictions(sub_html, subject)
                    # Merge scores
                    for ch, sc in sub_pred["chapter_scores"].items():
                        result["chapter_scores"][ch] = result["chapter_scores"].get(ch, 0) + sc
                    result["important_topics"].extend(sub_pred["important_topics"])
    
    # Cache results
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps(result, indent=2))
    
    return result

def scrape_education_blogs(subjects: list[str], force: bool = False) -> dict[str, dict]:
    """Scrape all education blogs for all subjects."""
    results = {s: {"chapter_scores": Counter(), "blog_breakdown": {}, "important_topics": []} 
               for s in subjects}
    
    for blog_name, blog_url in EDUCATION_BLOGS.items():
        print(f"  [blog] {blog_name}...", end=" ", flush=True)
        
        for subject in subjects:
            data = _scrape_blog(blog_name, blog_url, subject, force=force)
            
            # Aggregate chapter scores
            for chapter, score in data.get("chapter_scores", {}).items():
                results[subject]["chapter_scores"][chapter] += score
            
            # Track per-blog breakdown
            if data.get("chapter_scores"):
                results[subject]["blog_breakdown"][blog_name] = data["chapter_scores"]
            
            # Collect important topics
            results[subject]["important_topics"].extend(data.get("important_topics", []))
        
        print("done")
    
    # Normalize and finalize
    for subject in subjects:
        results[subject]["chapter_scores"] = dict(results[subject]["chapter_scores"].most_common(20))
        results[subject]["important_topics"] = list(set(results[subject]["important_topics"]))[:30]
    
    return results


def get_blog_signal(subjects: list[str], force: bool = False) -> dict[str, dict]:
    """Get normalized blog signals for scorer integration."""
    raw = scrape_education_blogs(subjects, force=force)
    
    normalized = {}
    for subject in subjects:
        chapter_scores = raw[subject]["chapter_scores"]
        if not chapter_scores:
            normalized[subject] = {}
            continue
        
        max_score = max(chapter_scores.values())
        normalized[subject] = {
            ch: round(sc / max_score, 4) for ch, sc in chapter_scores.items()
        } if max_score > 0 else {}
    
    return normalized
