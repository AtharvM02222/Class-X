"""config.py — master configuration for CBSE Class 10 Board Predictor 2027."""
import os
from pathlib import Path

# ── Target Year ───────────────────────────────────────────────────────────────
TARGET_YEAR = 2027  # Board Exam Year (Session 2026-27)
CURRENT_SESSION = "2026-27"

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
PAPERS_DIR  = DATA_DIR / "papers"
CACHE_DIR   = DATA_DIR / "cache"
RAW_DIR     = DATA_DIR / "raw"
OUTPUT_DIR  = BASE_DIR / "output"
PREBOARD_DIR = DATA_DIR / "preboard"
EXEMPLAR_DIR = DATA_DIR / "exemplar"
CASE_STUDY_DIR = DATA_DIR / "case_studies"
AR_BANK_DIR = DATA_DIR / "ar_bank"
for _d in [PAPERS_DIR, CACHE_DIR, RAW_DIR, OUTPUT_DIR, PREBOARD_DIR, EXEMPLAR_DIR,
           CASE_STUDY_DIR, AR_BANK_DIR,
           PAPERS_DIR/"science", PAPERS_DIR/"math", PAPERS_DIR/"social_science",
           PREBOARD_DIR/"science", PREBOARD_DIR/"math", PREBOARD_DIR/"social_science"]:
    _d.mkdir(parents=True, exist_ok=True)

# ── API Keys ──────────────────────────────────────────────────────────────────
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY", "")  # For ensemble
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")  # For ensemble

# ── Model Configuration ───────────────────────────────────────────────────────
GEMINI_MODEL      = "gemini-2.5-flash"
GEMINI_PRO        = "gemini-2.5-pro"  # For complex analysis
GEMINI_FLASH      = "gemini-2.0-flash"
GEMINI_TEMP       = 0.35
GEMINI_MAX_TOKENS = 16384  # Increased for longer outputs

# Ensemble models (when API keys available)
ENSEMBLE_MODELS = {
    "gemini": {"model": "gemini-2.5-flash", "weight": 0.45},
    "gpt4": {"model": "gpt-4-turbo", "weight": 0.35},
    "claude": {"model": "claude-3-sonnet", "weight": 0.20},
}

# ── Subjects ──────────────────────────────────────────────────────────────────
SUBJECTS = ["science", "math", "social_science"]
SUBJECT_DISPLAY = {
    "science":        "Science",
    "math":           "Mathematics",
    "social_science": "Social Science (SST)",
}
SUBJECT_CODES = {
    "science":        ["086","science","sci","physics","chemistry","biology","natural science","phy","chem","bio"],
    "math":           ["041","math","maths","mathematics","arithmetic","algebra","geometry","trigonometry","calculus"],
    "social_science": ["087","sst","social","history","geography","civics","economics","geo","hist","pol","political science","eco"],
}

# ── YouTube channels (EXPANDED - 15+ channels) ──────────────────────────────
YT_CHANNELS = {
    # Original channels
    "next_toppers":     "https://www.youtube.com/@NextToppers23/videos",
    "digraj_singh":     "https://www.youtube.com/@DigrajSinghRajput214/videos",
    "exp_hub":          "https://www.youtube.com/@exphub10th/videos",       # Prashant Kirad
    "shobhit_nirwan":   "https://www.youtube.com/@MathsByShobhitNirwan/videos",
    
    # Major Education Platforms
    "physics_wallah":   "https://www.youtube.com/@PhysicsWallah/videos",
    "pw_class10":       "https://www.youtube.com/@PW-Class10/videos",
    "vedantu_class10":  "https://www.youtube.com/@VedantuClass910/videos",
    "unacademy_10":     "https://www.youtube.com/@UnacademyClass9and10/videos",
    "byju_class10":     "https://www.youtube.com/@BYJUSClass10/videos",
    
    # Popular Individual Educators
    "magnet_brains":    "https://www.youtube.com/@MagnetBrains/videos",
    "dear_sir":         "https://www.youtube.com/@DearSir/videos",
    "science_and_fun":  "https://www.youtube.com/@ScienceandFunEducation/videos",
    "cbse_guru":        "https://www.youtube.com/@cbseguru/videos",
    "learncbse":        "https://www.youtube.com/@LearnCBSEVideos/videos",
    
    # Subject Specialists
    "maths_ncert":      "https://www.youtube.com/@MathsNCERTSolutions/videos",
    "science_sir":      "https://www.youtube.com/@ScienceSir10th/videos",
    "sst_expert":       "https://www.youtube.com/@SSTbyMukulSir/videos",
    "green_board":      "https://www.youtube.com/@GreenBoard/videos",
    
    # Regional/Exam Focused
    "exam_fear":        "https://www.youtube.com/@Abortyoutube/videos",
    "padhle":           "https://www.youtube.com/@Padhle/videos",
}
YT_MAX_VIDEOS = 300  # Increased from 200
YT_KEYWORDS = [
    # Prediction keywords
    "most important","imp questions","important questions","board exam",
    "2026 board","2027 board","sure shot","guaranteed","prediction","guess paper",
    "100 percent","must do","previous year","pyq","repeat","likely",
    "exam special","last minute","crash course","revision","one shot",
    "important chapters","high weightage","sure questions","board 2026","board 2027",
    # New NEP/Competency keywords
    "competency based","case study","assertion reason","hots","application based",
    "new pattern","changed pattern","nep 2020","cbse new format",
    # Confidence keywords
    "definitely coming","pakka aayega","100% aayega","zaroor aayega",
    "repeat question","asked every year","never miss","top priority",
    # Chapter-specific signals
    "most scoring","easy marks","scoring chapter","high marks",
]

# ── CBSE URLs (EXPANDED) ──────────────────────────────────────────────────────
CBSE_BASE = "https://cbseacademic.nic.in"
CBSE_URLS = {
    # Sample Question Papers
    "sqp_2026":    f"{CBSE_BASE}/SQP_CLASSX_2025-26.html",
    "sqp_2025":    f"{CBSE_BASE}/SQP_CLASSX_2024-25.html",
    "sqp_2024":    f"{CBSE_BASE}/SQP_CLASSX_2023-24.html",
    "sqp_2023":    f"{CBSE_BASE}/SQP_CLASSX_2022-23.html",
    
    # Previous Year Papers (last 6 years)
    "pyq_2025":    f"{CBSE_BASE}/Question_Paper_Classwise_2025.html",
    "pyq_2024":    f"{CBSE_BASE}/Question_Paper_Classwise_2024.html",
    "pyq_2023":    f"{CBSE_BASE}/Question_Paper_Classwise_2023.html",
    "pyq_2022":    f"{CBSE_BASE}/Question_Paper_Classwise_2022.html",
    "pyq_2020":    f"{CBSE_BASE}/Question_Paper_Classwise_2020.html",
    "pyq_2019":    f"{CBSE_BASE}/Question_Paper_Classwise_2019.html",
    
    # Marking Schemes
    "marking_2025": f"{CBSE_BASE}/Marking_Scheme_Classx_2025.html",
    "marking_2024": f"{CBSE_BASE}/Marking_Scheme_Classx.html",
    "marking_2023": f"{CBSE_BASE}/Marking_Scheme_Classx_2023.html",
    
    # Topper Scripts (gold mine for understanding what examiners want)
    "topper_2025": f"{CBSE_BASE}/Topper_Answer_Script_ClassX_2025.html",
    "topper_2024": f"{CBSE_BASE}/Topper_Answer_Script_ClassX.html",
    "topper_2023": f"{CBSE_BASE}/Topper_Answer_Script_ClassX_2023.html",
    
    # Syllabus & Curriculum
    "syllabus_2027": f"{CBSE_BASE}/Curriculum_2026-27.html",
    "syllabus_2026": f"{CBSE_BASE}/Curriculum_2025-26.html",
    "syllabus":      f"{CBSE_BASE}/Curriculum_2025.html",
    
    # Competency-Based Questions (NEP 2020)
    "competency":   f"{CBSE_BASE}/Competency_Based_Questions_ClassX.html",
}

# ── Education Blogs & Resources ───────────────────────────────────────────────
EDUCATION_BLOGS = {
    "learncbse":       "https://www.learncbse.in/class-10/",
    "mycbseguide":     "https://mycbseguide.com/blog/category/cbse-class-10/",
    "vedantu":         "https://www.vedantu.com/cbse/important-questions-class-10",
    "topperlearning":  "https://www.topperlearning.com/cbse-class-10",
    "byjus":           "https://byjus.com/cbse-notes/class-10/",
    "extramarks":      "https://www.extramarks.com/ncert-solutions/cbse-class-10",
    "teachoo":         "https://www.teachoo.com/subjects/class-10th/",
    "dronstudy":       "https://www.dronstudy.com/class-10/",
    "ncerthelp":       "https://www.ncerthelp.com/class-10/",
}

# ── Reddit/Forum Sources ──────────────────────────────────────────────────────
REDDIT_SUBREDDITS = [
    "CBSE",
    "IndianStudents", 
    "Indian_Academia",
    "cbse_class_10",
    "JEENEETards",  # Often discusses board prep too
]

# ── Pre-Board Paper Sources ───────────────────────────────────────────────────
PREBOARD_SOURCES = {
    "kv_papers":       "https://www.cbseboardonline.com/sample-papers/kv-pre-board/",
    "dps_papers":      "https://www.cbseboardonline.com/sample-papers/dps-pre-board/",
    "dav_papers":      "https://www.davkk.in/downloads-sample-papers.html",
    "navodaya_papers": "https://www.navodaya.gov.in/nvs/en/Examination-Materials/",
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

# ── NCERT Exemplar PDFs (HIGH VALUE - these get converted to board questions) ─
NCERT_EXEMPLAR = {
    "science": [
        "https://ncert.nic.in/exemplar/pdf/jeesc101.pdf",  # Chemical Reactions
        "https://ncert.nic.in/exemplar/pdf/jeesc102.pdf",  # Acids, Bases, Salts
        "https://ncert.nic.in/exemplar/pdf/jeesc103.pdf",  # Metals Non-metals
        "https://ncert.nic.in/exemplar/pdf/jeesc104.pdf",  # Carbon Compounds
        "https://ncert.nic.in/exemplar/pdf/jeesc105.pdf",  # Life Processes
        "https://ncert.nic.in/exemplar/pdf/jeesc106.pdf",  # Control Coordination
        "https://ncert.nic.in/exemplar/pdf/jeesc107.pdf",  # Reproduction
        "https://ncert.nic.in/exemplar/pdf/jeesc108.pdf",  # Heredity
        "https://ncert.nic.in/exemplar/pdf/jeesc109.pdf",  # Light
        "https://ncert.nic.in/exemplar/pdf/jeesc110.pdf",  # Human Eye
        "https://ncert.nic.in/exemplar/pdf/jeesc111.pdf",  # Electricity
        "https://ncert.nic.in/exemplar/pdf/jeesc112.pdf",  # Magnetic Effects
        "https://ncert.nic.in/exemplar/pdf/jeesc113.pdf",  # Environment
        "https://ncert.nic.in/exemplar/pdf/jeesc114.pdf",  # Natural Resources
    ],
    "math": [
        "https://ncert.nic.in/exemplar/pdf/jeemh101.pdf",  # Real Numbers
        "https://ncert.nic.in/exemplar/pdf/jeemh102.pdf",  # Polynomials
        "https://ncert.nic.in/exemplar/pdf/jeemh103.pdf",  # Linear Equations
        "https://ncert.nic.in/exemplar/pdf/jeemh104.pdf",  # Quadratic Equations
        "https://ncert.nic.in/exemplar/pdf/jeemh105.pdf",  # AP
        "https://ncert.nic.in/exemplar/pdf/jeemh106.pdf",  # Triangles
        "https://ncert.nic.in/exemplar/pdf/jeemh107.pdf",  # Coordinate Geometry
        "https://ncert.nic.in/exemplar/pdf/jeemh108.pdf",  # Trigonometry Intro
        "https://ncert.nic.in/exemplar/pdf/jeemh109.pdf",  # Trig Applications
        "https://ncert.nic.in/exemplar/pdf/jeemh110.pdf",  # Circles
        "https://ncert.nic.in/exemplar/pdf/jeemh111.pdf",  # Areas Circles
        "https://ncert.nic.in/exemplar/pdf/jeemh112.pdf",  # Surface Volumes
        "https://ncert.nic.in/exemplar/pdf/jeemh113.pdf",  # Statistics
        "https://ncert.nic.in/exemplar/pdf/jeemh114.pdf",  # Probability
    ],
}

# ── Scoring weights (EXPANDED - must sum to 1.0) ──────────────────────────────
WEIGHTS = {
    "blueprint":       0.18,   # Official CBSE marks allocation
    "pyq_frequency":   0.16,   # Past paper chapter frequency
    "year_trend":      0.10,   # Recency-weighted trajectory
    "gap_bonus":       0.12,   # Overdue chapter bonus (INCREASED)
    "yt_mentions":     0.12,   # YouTube prediction consensus
    "yt_prediction":   0.06,   # Specific "sure shot" video signals
    "ncert_density":   0.05,   # NCERT exercise count
    "unit_balance":    0.04,   # Under-represented unit boost
    # NEW SIGNALS
    "preboard_signal": 0.06,   # Pre-board paper patterns (DPS/KV/DAV)
    "blog_consensus":  0.04,   # Education blog predictions
    "difficulty_prog": 0.03,   # Difficulty progression trend
    "examiner_pref":   0.02,   # Examiner behavior from marking schemes
    "competency_map":  0.02,   # NEP competency-based question mapping
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 0.001, f"Weights must sum to 1.0, got {sum(WEIGHTS.values())}"

# ── Output ────────────────────────────────────────────────────────────────────
CONFIDENCE_BANDS = {"High": 0.65, "Medium": 0.40, "Low": 0.0}  # Adjusted thresholds
QUESTION_DISTRIBUTION = {   # questions per mark type per subject (updated 2026-27)
    "science":        {1: 20, 2: 6, 3: 7, 5: 3},   # Total: 80 marks
    "math":           {1: 20, 2: 5, 3: 6, 4: 4},   # Total: 80 marks
    "social_science": {1: 20, 3: 5, 5: 5},         # Total: 80 marks
}

# ── NEP 2020 Competency Categories ────────────────────────────────────────────
COMPETENCY_TYPES = {
    "knowledge":        {"weight": 0.20, "desc": "Recall, define, list, state"},
    "understanding":    {"weight": 0.25, "desc": "Explain, compare, distinguish"},
    "application":      {"weight": 0.30, "desc": "Apply, calculate, solve, use"},
    "analysis":         {"weight": 0.15, "desc": "Analyze, differentiate, relate"},
    "evaluation":       {"weight": 0.10, "desc": "Evaluate, justify, assess"},
}

# ── Case Study Configuration ──────────────────────────────────────────────────
CASE_STUDY_CONFIG = {
    "science": {
        "min_passage_words": 80,
        "max_passage_words": 150,
        "sub_questions": 4,
        "marks_per_case": 4,
        "num_cases": 2,
    },
    "math": {
        "min_passage_words": 60,
        "max_passage_words": 120,
        "sub_questions": 5,
        "marks_per_case": 4,
        "num_cases": 2,
    },
    "social_science": {
        "min_passage_words": 100,
        "max_passage_words": 200,
        "sub_questions": 5,
        "marks_per_case": 5,
        "num_cases": 1,
    },
}

# ── Assertion-Reason Configuration ────────────────────────────────────────────
AR_CONFIG = {
    "science": {"count": 2, "marks": 1},
    "math": {"count": 2, "marks": 1},
    "social_science": {"count": 2, "marks": 1},
}

# ── HTTP ──────────────────────────────────────────────────────────────────────
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
HTTP_TIMEOUT  = 30
HTTP_DELAY    = 0.5
HTTP_RETRIES  = 5

# ── Practice Paper Generator Settings ─────────────────────────────────────────
PAPER_TEMPLATES = {
    "full_paper": {"duration": "3 hours", "total_marks": 80},
    "half_paper": {"duration": "1.5 hours", "total_marks": 40},
    "chapter_test": {"duration": "45 mins", "total_marks": 25},
}

# ── Export Settings ───────────────────────────────────────────────────────────
EXPORT_FORMATS = ["json", "txt", "html", "pdf", "md"]
HTML_TEMPLATE_DIR = OUTPUT_DIR / "templates"
