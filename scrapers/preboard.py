"""scrapers/preboard.py — aggregates pre-board papers from DPS, KV, DAV, Navodaya."""
import json, re, sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import PREBOARD_SOURCES, PREBOARD_DIR, SUBJECT_CODES, TARGET_YEAR
from scrapers.http import fetch_text, fetch_binary

def _cache_path(source: str) -> Path:
    from config import CACHE_DIR
    return CACHE_DIR / f"preboard_{source}.json"

def _is_class10(text: str) -> bool:
    """Check if text refers to Class 10."""
    t = text.lower()
    return any(x in t for x in [
        "class x", "class-x", "classx", "_x_", "_x.", "10th", "x_2",
        "std x", "grade x", "secondary", "class 10"
    ])

def _subject_match(text: str, subject: str) -> bool:
    """Check if text matches a subject."""
    t = text.lower()
    return any(c in t for c in SUBJECT_CODES[subject])

def _year_match(text: str) -> bool:
    """Check if text is for recent years."""
    t = text.lower()
    return any(str(y) in t for y in range(TARGET_YEAR - 2, TARGET_YEAR + 1))

def _collect_pdf_links(html: str, base_url: str, subject: str) -> list[dict]:
    """Extract PDF links from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.lower().endswith(".pdf"):
            continue
        
        label = a.get_text(" ", strip=True)
        combo = (label + " " + href).lower()
        
        # Check if it matches our criteria
        if _is_class10(combo) and _subject_match(combo, subject):
            # Prefer recent years
            priority = 2 if _year_match(combo) else 1
            
            # Check for pre-board indicators
            if any(kw in combo for kw in ["pre-board", "preboard", "pre board", "practice", "mock"]):
                priority += 1
            
            links.append({
                "url": urljoin(base_url, href),
                "label": label or href.split("/")[-1],
                "priority": priority,
            })
    
    # Sort by priority (highest first)
    links.sort(key=lambda x: -x["priority"])
    return links

def _safe_filename(label: str, source: str) -> str:
    """Create a safe filename from label."""
    name = re.sub(r"[^\w\-.]", "_", label)[:70]
    name = f"{source}_{name}"
    return name if name.endswith(".pdf") else name + ".pdf"

def scrape_preboard_papers(subjects: list[str], force: bool = False) -> dict[str, list[Path]]:
    """Scrape pre-board papers from all sources."""
    downloaded = {s: [] for s in subjects}
    
    for source_name, source_url in PREBOARD_SOURCES.items():
        print(f"  [preboard] {source_name}...", end=" ", flush=True)
        
        # Check cache
        cp = _cache_path(source_name)
        cached_links = {}
        if cp.exists() and not force:
            try:
                cached_links = json.loads(cp.read_text())
            except:
                pass
        
        # Fetch the source page
        html = fetch_text(source_url, force=force)
        if not html:
            print("failed to fetch")
            continue
        
        source_downloads = 0
        
        for subject in subjects:
            # Get PDF links for this subject
            links = _collect_pdf_links(html, source_url, subject)
            
            # Try to follow sub-pages for more papers
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                link_text = a.get_text(" ", strip=True).lower()
                href = a["href"]
                
                # Look for pages that might have more papers
                if any(kw in link_text for kw in ["sample paper", "question paper", "pre board", "class x", "class 10"]):
                    sub_url = urljoin(source_url, href)
                    if sub_url != source_url and sub_url.endswith((".html", ".htm", ".php", ".aspx", "/")):
                        sub_html = fetch_text(sub_url)
                        if sub_html:
                            sub_links = _collect_pdf_links(sub_html, sub_url, subject)
                            links.extend(sub_links)
            
            # Deduplicate by URL
            seen_urls = set()
            unique_links = []
            for link in links:
                if link["url"] not in seen_urls:
                    seen_urls.add(link["url"])
                    unique_links.append(link)
            
            # Download PDFs (limit to top 10 per source per subject)
            for link in unique_links[:10]:
                dest = PREBOARD_DIR / subject / _safe_filename(link["label"], source_name)
                
                if dest.exists() and not force:
                    downloaded[subject].append(dest)
                    continue
                
                if fetch_binary(link["url"], dest, force=force):
                    downloaded[subject].append(dest)
                    source_downloads += 1
        
        print(f"{source_downloads} papers")
        
        # Update cache
        from config import CACHE_DIR
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps({"downloaded": source_downloads}, indent=2))
    
    # Also include any manually placed pre-board papers
    for subject in subjects:
        subdir = PREBOARD_DIR / subject
        if subdir.exists():
            for f in subdir.glob("*.pdf"):
                if f not in downloaded[subject]:
                    downloaded[subject].append(f)
    
    return downloaded


def get_preboard_analysis(subjects: list[str], force: bool = False) -> dict[str, dict]:
    """Get pre-board paper analysis for scoring."""
    from analyzers.pdf import analyze_pdfs
    
    papers = scrape_preboard_papers(subjects, force=force)
    
    results = {}
    for subject in subjects:
        if papers.get(subject):
            print(f"  [preboard] Analyzing {len(papers[subject])} {subject} papers...")
            analysis = analyze_pdfs(papers[subject], subject)
            results[subject] = {
                "chapter_freq": analysis.get("chapter_freq", {}),
                "total_papers": len(papers[subject]),
            }
        else:
            results[subject] = {"chapter_freq": {}, "total_papers": 0}
    
    return results


def get_preboard_signal(subjects: list[str], force: bool = False) -> dict[str, dict]:
    """Get normalized pre-board signals for scorer integration."""
    raw = get_preboard_analysis(subjects, force=force)
    
    normalized = {}
    for subject in subjects:
        chapter_freq = raw[subject].get("chapter_freq", {})
        if not chapter_freq:
            normalized[subject] = {}
            continue
        
        max_freq = max(chapter_freq.values())
        normalized[subject] = {
            ch: round(freq / max_freq, 4) for ch, freq in chapter_freq.items()
        } if max_freq > 0 else {}
    
    return normalized
