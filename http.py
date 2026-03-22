"""scrapers/http.py — shared HTTP session with retry backoff, disk cache, rate-limit."""
import hashlib, json, time, sys
from pathlib import Path
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import CACHE_DIR, HTTP_HEADERS, HTTP_TIMEOUT, HTTP_DELAY, HTTP_RETRIES

_session: Optional[requests.Session] = None

def _get_session() -> requests.Session:
    global _session
    if _session: return _session
    s = requests.Session()
    retry = Retry(total=HTTP_RETRIES, backoff_factor=1.5,
                  status_forcelist=[429,500,502,503,504],
                  allowed_methods=["GET"])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://",  HTTPAdapter(max_retries=retry))
    s.headers.update(HTTP_HEADERS)
    _session = s
    return s

def _cache_file(url: str) -> Path:
    return CACHE_DIR / f"http_{hashlib.md5(url.encode()).hexdigest()}.json"

def fetch_text(url: str, use_cache: bool = True, force: bool = False) -> Optional[str]:
    cf = _cache_file(url)
    if use_cache and not force and cf.exists():
        try: return json.loads(cf.read_text())["body"]
        except: pass
    try:
        r = _get_session().get(url, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        body = r.text
        if use_cache:
            cf.write_text(json.dumps({"url": url, "body": body, "ts": time.time()}))
        time.sleep(HTTP_DELAY)
        return body
    except Exception as e:
        print(f"  [http] FAIL {url[:70]}: {e}")
        return None

def fetch_binary(url: str, dest: Path, force: bool = False) -> bool:
    if dest.exists() and not force and dest.stat().st_size > 1024:
        return True
    try:
        r = _get_session().get(url, timeout=40, stream=True)
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in r.iter_content(8192): f.write(chunk)
        time.sleep(HTTP_DELAY)
        return True
    except Exception as e:
        print(f"  [http] download FAIL {url[:70]}: {e}")
        return False
