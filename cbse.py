"""scrapers/cbse.py — scrapes cbseacademic.nic.in: SQP, PYQ, marking, topper answer scripts."""
import re, sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import CBSE_URLS, CBSE_BASE, PAPERS_DIR, SUBJECT_CODES
from scrapers.http import fetch_text, fetch_binary

def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def _is_class10(text: str) -> bool:
    t = text.lower()
    return any(x in t for x in ["class x","class-x","classx","_x_","_x.","10th","x_2","std x","grade x","secondary"])

def _subject_match(text: str, subject: str) -> bool:
    t = text.lower()
    return any(c in t for c in SUBJECT_CODES[subject])

def _collect_pdf_links(html: str, base: str, subject: str) -> list[dict]:
    soup = _soup(html)
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.lower().endswith(".pdf"): continue
        label = a.get_text(" ", strip=True)
        combo = (label + " " + href).lower()
        if _is_class10(combo) and _subject_match(combo, subject):
            links.append({"url": urljoin(base, href), "label": label or href.split("/")[-1]})
    return links

def _follow_and_collect(html: str, base: str, subject: str, depth: int = 1) -> list[dict]:
    """Follow year-specific sub-pages to find more PDFs."""
    if depth == 0: return []
    soup = _soup(html)
    links = _collect_pdf_links(html, base, subject)
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True).lower()
        href = a["href"]
        if not href.lower().endswith((".html",".htm",".asp",".aspx")): continue
        if any(x in text for x in ["class x","class 10","2025","2024","2023","sample","question","marking"]):
            sub_url  = urljoin(base, href)
            sub_html = fetch_text(sub_url)
            if sub_html:
                links += _follow_and_collect(sub_html, base, subject, depth - 1)
    # deduplicate by URL
    seen = set(); unique = []
    for l in links:
        if l["url"] not in seen:
            seen.add(l["url"]); unique.append(l)
    return unique

def _safe_filename(label: str) -> str:
    name = re.sub(r"[^\w\-.]", "_", label)[:90]
    return name if name.endswith(".pdf") else name + ".pdf"

def scrape_cbse(subjects: list[str], force: bool = False) -> dict[str, list[Path]]:
    downloaded: dict[str, list[Path]] = {s: [] for s in subjects}
    for source_name, url in CBSE_URLS.items():
        print(f"  [cbse] {source_name}: {url.split('/')[-1]}")
        html = fetch_text(url, force=force)
        if not html: continue
        for subject in subjects:
            links = _follow_and_collect(html, CBSE_BASE, subject, depth=1)
            for lnk in links:
                dest = PAPERS_DIR / subject / _safe_filename(lnk["label"])
                if fetch_binary(lnk["url"], dest, force=force):
                    if dest not in downloaded[subject]:
                        downloaded[subject].append(dest)
                        print(f"    ✓ {subject}/{dest.name}")
    # Collect any manually placed PDFs
    for subject in subjects:
        subdir = PAPERS_DIR / subject
        if subdir.exists():
            for f in subdir.glob("*.pdf"):
                if f not in downloaded[subject]: downloaded[subject].append(f)
    return downloaded
