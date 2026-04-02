"""signals/difficulty.py — difficulty progression tracking across years."""
import sys
from pathlib import Path
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).parent.parent))
from blueprint import BLUEPRINT, HISTORY
from config import TARGET_YEAR

# Difficulty indicators in question text
DIFFICULTY_KEYWORDS = {
    "easy": ["define", "list", "name", "state", "what is", "write", "mention", "give example"],
    "medium": ["explain", "describe", "differentiate", "compare", "distinguish", "how", "why"],
    "hard": ["analyse", "evaluate", "derive", "prove", "design", "calculate", "numerical", "critical"],
    "application": ["apply", "solve", "find", "calculate", "determine", "word problem", "case study"],
}

def analyze_difficulty_trend(pdf_analysis: dict) -> dict[str, dict]:
    """Analyze how difficulty has evolved for each chapter over years."""
    trends = {}
    
    for subject, data in pdf_analysis.items():
        chapter_trends = {}
        year_data = data.get("year_data", {})
        questions = data.get("questions", [])
        
        # Build year-wise difficulty profile for each chapter
        chapter_year_difficulty = defaultdict(lambda: defaultdict(list))
        
        for q in questions:
            chapter = q.get("chapter", "")
            year = q.get("year", 0)
            qtype = q.get("type", "")
            text = q.get("q", "").lower()
            
            if not chapter or not year:
                continue
            
            # Estimate difficulty from question type and keywords
            difficulty_score = 0
            
            # Type-based scoring
            type_scores = {"MCQ": 1, "SA1": 2, "SA2": 3, "LA": 4, "CASE": 4}
            difficulty_score += type_scores.get(qtype, 2)
            
            # Keyword-based scoring
            for level, keywords in DIFFICULTY_KEYWORDS.items():
                if any(kw in text for kw in keywords):
                    if level == "easy":
                        difficulty_score -= 0.5
                    elif level == "hard":
                        difficulty_score += 1
                    elif level == "application":
                        difficulty_score += 0.5
            
            chapter_year_difficulty[chapter][year].append(difficulty_score)
        
        # Calculate trends
        for chapter in BLUEPRINT[subject]["chapters"]:
            if BLUEPRINT[subject]["chapters"][chapter].get("deleted"):
                continue
            
            year_difficulties = chapter_year_difficulty.get(chapter, {})
            
            if len(year_difficulties) < 2:
                chapter_trends[chapter] = {
                    "trend": "stable",
                    "current_difficulty": "medium",
                    "trend_score": 0.0,
                }
                continue
            
            # Calculate average difficulty per year
            year_avgs = {}
            for year, scores in year_difficulties.items():
                if scores:
                    year_avgs[year] = sum(scores) / len(scores)
            
            if len(year_avgs) < 2:
                chapter_trends[chapter] = {
                    "trend": "stable",
                    "current_difficulty": "medium",
                    "trend_score": 0.0,
                }
                continue
            
            # Sort by year and calculate trend
            sorted_years = sorted(year_avgs.keys())
            recent_years = sorted_years[-3:]  # Last 3 years
            
            if len(recent_years) >= 2:
                # Simple linear trend
                recent_avgs = [year_avgs[y] for y in recent_years]
                trend_score = (recent_avgs[-1] - recent_avgs[0]) / len(recent_avgs)
            else:
                trend_score = 0.0
            
            # Determine trend direction
            if trend_score > 0.3:
                trend = "increasing"
            elif trend_score < -0.3:
                trend = "decreasing"
            else:
                trend = "stable"
            
            # Current difficulty level
            current_avg = year_avgs.get(max(year_avgs.keys()), 2.5)
            if current_avg < 2:
                current_difficulty = "easy"
            elif current_avg < 3:
                current_difficulty = "medium"
            else:
                current_difficulty = "hard"
            
            chapter_trends[chapter] = {
                "trend": trend,
                "current_difficulty": current_difficulty,
                "trend_score": round(trend_score, 3),
                "year_averages": {str(y): round(a, 2) for y, a in year_avgs.items()},
            }
        
        trends[subject] = chapter_trends
    
    return trends


def get_difficulty_signal(subjects: list[str], pdf_analysis: dict) -> dict[str, dict]:
    """Get normalized difficulty progression signal for scorer."""
    trends = analyze_difficulty_trend(pdf_analysis)
    
    signals = {}
    for subject in subjects:
        chapter_signals = {}
        
        for chapter, data in trends.get(subject, {}).items():
            # Increasing difficulty = higher signal (more likely to be important)
            # Hard chapters that are getting harder = very likely to appear
            trend_score = data.get("trend_score", 0)
            
            # Convert trend to signal
            if data.get("trend") == "increasing":
                signal = 0.6 + min(0.4, trend_score)
            elif data.get("trend") == "decreasing":
                signal = 0.3 - min(0.2, abs(trend_score))
            else:
                signal = 0.5
            
            # Boost hard chapters slightly (they often appear as LA)
            if data.get("current_difficulty") == "hard":
                signal += 0.1
            
            chapter_signals[chapter] = round(min(1.0, max(0.0, signal)), 4)
        
        # Normalize
        if chapter_signals:
            max_sig = max(chapter_signals.values())
            if max_sig > 0:
                chapter_signals = {ch: round(s / max_sig, 4) for ch, s in chapter_signals.items()}
        
        signals[subject] = chapter_signals
    
    return signals
