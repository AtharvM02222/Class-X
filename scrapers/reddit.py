"""scrapers/reddit.py — extracts prediction signals from Reddit discussions."""
import json, re, sys
from pathlib import Path
from collections import Counter
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import REDDIT_SUBREDDITS, CACHE_DIR, SUBJECT_CODES, TARGET_YEAR
from scrapers.http import fetch_text

REDDIT_API = "https://www.reddit.com"

def _cache_path(subreddit: str) -> Path:
    return CACHE_DIR / f"reddit_{subreddit}.json"

def _extract_chapter_mentions(text: str, subject: str) -> dict[str, float]:
    """Extract chapter mentions from Reddit text with confidence scores."""
    from blueprint import BLUEPRINT
    
    text_lower = text.lower()
    chapter_scores = Counter()
    
    # Prediction keywords that boost confidence
    boost_keywords = [
        "definitely", "surely", "100%", "guaranteed", "will come", "must prepare",
        "important", "expected", "prediction", "sure shot", "high chance",
        str(TARGET_YEAR), "board", "cbse", "exam"
    ]
    
    for chapter, data in BLUEPRINT[subject]["chapters"].items():
        if data.get("deleted"):
            continue
        
        # Base scoring on chapter name
        chapter_words = [w for w in chapter.lower().split() if len(w) > 3]
        word_hits = sum(1 for w in chapter_words if w in text_lower)
        
        if word_hits < 2:
            continue
        
        base_score = word_hits * 2
        
        # Key topic bonus
        topic_hits = sum(1 for t in data.get("key_topics", []) if t.lower() in text_lower)
        topic_score = topic_hits * 1.5
        
        # Boost keyword proximity bonus
        boost_score = 0
        for kw in boost_keywords:
            if kw in text_lower:
                # Check proximity to chapter mention
                for word in chapter_words:
                    pattern = rf"{re.escape(kw)}.{{0,100}}{re.escape(word)}"
                    if re.search(pattern, text_lower):
                        boost_score += 0.5
        
        total = base_score + topic_score + boost_score
        if total > 2:
            chapter_scores[chapter] = total
    
    return dict(chapter_scores)

def _fetch_subreddit_posts(subreddit: str, force: bool = False) -> list[dict]:
    """Fetch recent posts from a subreddit using JSON API."""
    cp = _cache_path(subreddit)
    if cp.exists() and not force:
        try:
            return json.loads(cp.read_text())
        except:
            pass
    
    posts = []
    
    # Fetch from Reddit's public JSON API (no auth needed)
    urls = [
        f"{REDDIT_API}/r/{subreddit}/search.json?q=board+exam+{TARGET_YEAR}&restrict_sr=on&sort=relevance&t=year&limit=50",
        f"{REDDIT_API}/r/{subreddit}/search.json?q=important+questions&restrict_sr=on&sort=relevance&t=year&limit=50",
        f"{REDDIT_API}/r/{subreddit}/search.json?q=prediction+{TARGET_YEAR}&restrict_sr=on&sort=relevance&t=year&limit=50",
        f"{REDDIT_API}/r/{subreddit}/hot.json?limit=50",
    ]
    
    for url in urls:
        try:
            response = fetch_text(url)
            if not response:
                continue
            
            data = json.loads(response)
            children = data.get("data", {}).get("children", [])
            
            for child in children:
                post_data = child.get("data", {})
                posts.append({
                    "title": post_data.get("title", ""),
                    "selftext": post_data.get("selftext", ""),
                    "score": post_data.get("score", 0),
                    "created_utc": post_data.get("created_utc", 0),
                    "num_comments": post_data.get("num_comments", 0),
                    "subreddit": subreddit,
                })
        except Exception as e:
            print(f"    [reddit] Error fetching {subreddit}: {e}")
    
    # Deduplicate by title
    seen_titles = set()
    unique_posts = []
    for post in posts:
        if post["title"] not in seen_titles:
            seen_titles.add(post["title"])
            unique_posts.append(post)
    
    # Cache results
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps(unique_posts, indent=2))
    
    return unique_posts

def _is_relevant_post(post: dict, subject: str) -> bool:
    """Check if a post is relevant to a subject."""
    text = (post.get("title", "") + " " + post.get("selftext", "")).lower()
    return any(code in text for code in SUBJECT_CODES[subject])

def scrape_reddit(subjects: list[str], force: bool = False) -> dict[str, dict]:
    """Scrape Reddit for exam prediction signals."""
    results = {s: {
        "chapter_scores": Counter(),
        "top_posts": [],
        "total_mentions": 0,
        "subreddit_breakdown": {},
    } for s in subjects}
    
    all_posts = []
    
    for subreddit in REDDIT_SUBREDDITS:
        print(f"  [reddit] r/{subreddit}...", end=" ", flush=True)
        posts = _fetch_subreddit_posts(subreddit, force=force)
        all_posts.extend(posts)
        print(f"{len(posts)} posts")
    
    # Process posts for each subject
    for post in all_posts:
        full_text = post.get("title", "") + " " + post.get("selftext", "")
        
        # Weight by engagement
        engagement_weight = 1 + (post.get("score", 0) / 100) + (post.get("num_comments", 0) / 50)
        engagement_weight = min(engagement_weight, 3.0)  # Cap at 3x
        
        for subject in subjects:
            if not _is_relevant_post(post, subject):
                continue
            
            chapter_mentions = _extract_chapter_mentions(full_text, subject)
            
            for chapter, score in chapter_mentions.items():
                weighted_score = score * engagement_weight
                results[subject]["chapter_scores"][chapter] += weighted_score
            
            if chapter_mentions:
                results[subject]["total_mentions"] += 1
                
                # Track top posts
                if len(results[subject]["top_posts"]) < 15:
                    results[subject]["top_posts"].append({
                        "title": post.get("title", "")[:100],
                        "score": post.get("score", 0),
                        "chapters": list(chapter_mentions.keys())[:5],
                    })
    
    # Normalize and finalize
    for subject in subjects:
        results[subject]["chapter_scores"] = dict(
            results[subject]["chapter_scores"].most_common(20)
        )
        results[subject]["top_posts"] = sorted(
            results[subject]["top_posts"], 
            key=lambda x: -x.get("score", 0)
        )[:10]
    
    return results


def get_reddit_signal(subjects: list[str], force: bool = False) -> dict[str, dict]:
    """Get normalized Reddit signals for scorer integration."""
    raw = scrape_reddit(subjects, force=force)
    
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
