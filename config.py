"""config.py — master configuration for CBSE Class 10 Board Predictor."""
import os
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
PAPERS_DIR  = DATA_DIR / "papers"
CACHE_DIR   = DATA_DIR / "cache"
RAW_DIR     = DATA_DIR / "raw"
OUTPUT_DIR  = BASE_DIR / "output"
for _d in [PAPERS_DIR, CACHE_DIR, RAW_DIR, OUTPUT_DIR,
           PAPERS_DIR/"science", PAPERS_DIR/"math", PAPERS_DIR/"social_science"]:
    _d.mkdir(parents=True, exist_ok=True)

# ── API ───────────────────────────────────────────────────────────────────────
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL      = "gemini-1.5-pro"
GEMINI_FLASH      = "gemini-1.5-flash"
GEMINI_TEMP       = 0.35
GEMINI_MAX_TOK    = 8192

# ── Subjects ──────────────────────────────────────────────────────────────────
SUBJECTS = ["science", "math", "social_science"]
SUBJECT_DISPLAY = {
    "science":        "Science",
    "math":           "Mathematics",
    "social_science": "Social Science (SST)",
}
SUBJECT_CODES = {
    "science":        ["086","science","sci","physics","chemistry","biology","natural science"],
    "math":           ["041","math","maths","mathematics","arithmetic","algebra","geometry"],
    "social_science": ["087","sst","social","history","geography","civics","economics","geo","hist","pol"],
}

# ── YouTube channels (corrected) ─────────────────────────────────────────────
YT_CHANNELS = {
    "next_toppers":    "https://www.youtube.com/@NextToppers23/videos",
    "digraj_singh":    "https://www.youtube.com/@DigrajSinghRajput214/videos",
    "exp_hub":         "https://www.youtube.com/@exphub10th/videos",       # Prashant Kirad
    "shobhit_nirwan":  "https://www.youtube.com/@MathsByShobhitNirwan/videos",
}
YT_MAX_VIDEOS = 200
YT_KEYWORDS = [
    "most important","imp questions","important questions","board exam",
    "2025 board","sure shot","guaranteed","prediction","guess paper",
    "100 percent","must do","previous year","pyq","repeat","likely",
    "exam special","last minute","crash course","revision","one shot",
    "important chapters","high weightage","sure questions","board 2025",
]

# ── CBSE URLs ─────────────────────────────────────────────────────────────────
CBSE_BASE = "https://cbseacademic.nic.in"
CBSE_URLS = {
    "sqp_2025":    f"{CBSE_BASE}/SQP_CLASSX.html",
    "sqp_2024":    f"{CBSE_BASE}/SQP_CLASSX_2024.html",
    "pyq_2024":    f"{CBSE_BASE}/Question_Paper_Classwise_2024.html",
    "pyq_2023":    f"{CBSE_BASE}/Question_Paper_Classwise_2023.html",
    "pyq_2022":    f"{CBSE_BASE}/Question_Paper_Classwise_2022.html",
    "marking_2024":f"{CBSE_BASE}/Marking_Scheme_Classx.html",
    "topper_2024": f"{CBSE_BASE}/Topper_Answer_Script_ClassX.html",
    "syllabus":    f"{CBSE_BASE}/Curriculum_2025.html",
}

# ── NCERT PDF direct links (Class 10) ─────────────────────────────────────────
NCERT_PDFS = {
    "science": [
        "https://ncert.nic.in/textbook/pdf/jesc1.zip",
        "https://ncert.nic.in/textbook/pdf/jesc101.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc102.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc103.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc104.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc105.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc106.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc107.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc108.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc109.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc110.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc111.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc112.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc113.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc114.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc115.pdf",
        "https://ncert.nic.in/textbook/pdf/jesc116.pdf",
    ],
    "math": [
        "https://ncert.nic.in/textbook/pdf/jemh101.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh102.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh103.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh104.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh105.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh106.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh107.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh108.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh109.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh110.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh111.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh112.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh113.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh114.pdf",
        "https://ncert.nic.in/textbook/pdf/jemh115.pdf",
    ],
    "social_science": [
        # History - India and the Contemporary World II
        "https://ncert.nic.in/textbook/pdf/jhis301.pdf",
        "https://ncert.nic.in/textbook/pdf/jhis302.pdf",
        "https://ncert.nic.in/textbook/pdf/jhis303.pdf",
        "https://ncert.nic.in/textbook/pdf/jhis304.pdf",
        "https://ncert.nic.in/textbook/pdf/jhis305.pdf",
        # Geography - Contemporary India II
        "https://ncert.nic.in/textbook/pdf/jess301.pdf",
        "https://ncert.nic.in/textbook/pdf/jess302.pdf",
        "https://ncert.nic.in/textbook/pdf/jess303.pdf",
        "https://ncert.nic.in/textbook/pdf/jess304.pdf",
        "https://ncert.nic.in/textbook/pdf/jess305.pdf",
        "https://ncert.nic.in/textbook/pdf/jess306.pdf",
        "https://ncert.nic.in/textbook/pdf/jess307.pdf",
        # Civics - Democratic Politics II
        "https://ncert.nic.in/textbook/pdf/jpol301.pdf",
        "https://ncert.nic.in/textbook/pdf/jpol302.pdf",
        "https://ncert.nic.in/textbook/pdf/jpol303.pdf",
        "https://ncert.nic.in/textbook/pdf/jpol304.pdf",
        "https://ncert.nic.in/textbook/pdf/jpol305.pdf",
        "https://ncert.nic.in/textbook/pdf/jpol306.pdf",
        "https://ncert.nic.in/textbook/pdf/jpol307.pdf",
        "https://ncert.nic.in/textbook/pdf/jpol308.pdf",
        # Economics - Understanding Economic Development
        "https://ncert.nic.in/textbook/pdf/jeco301.pdf",
        "https://ncert.nic.in/textbook/pdf/jeco302.pdf",
        "https://ncert.nic.in/textbook/pdf/jeco303.pdf",
        "https://ncert.nic.in/textbook/pdf/jeco304.pdf",
        "https://ncert.nic.in/textbook/pdf/jeco305.pdf",
    ],
}

# ── Scoring weights (must sum to 1.0) ────────────────────────────────────────
WEIGHTS = {
    "blueprint":       0.22,
    "pyq_frequency":   0.20,
    "year_trend":      0.13,
    "gap_bonus":       0.10,
    "yt_mentions":     0.15,
    "yt_prediction":   0.08,
    "ncert_density":   0.07,
    "unit_balance":    0.05,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 0.001, "Weights must sum to 1.0"

# ── Output ────────────────────────────────────────────────────────────────────
CONFIDENCE_BANDS = {"High": 0.62, "Medium": 0.38, "Low": 0.0}
Q_DIST = {   # questions per mark type per subject
    "science":        {1: 20, 2: 6, 3: 7, 5: 3},
    "math":           {1: 20, 2: 5, 3: 6, 4: 4},
    "social_science": {1: 20, 3: 5, 5: 4},
}

# ── HTTP ──────────────────────────────────────────────────────────────────────
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}
HTTP_TIMEOUT  = 25
HTTP_DELAY    = 0.7
HTTP_RETRIES  = 4
