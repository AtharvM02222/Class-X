# CBSE Class 10 Board Exam Predictor 2027 — MEGA EDITION

An elite AI-powered exam intelligence system that predicts the **CBSE Class 10 Board Exam 2027** questions by fusing **10+ years of historical data**, official blueprint weights, **20+ YouTube educator signals**, Reddit community intelligence, education blog consensus, pre-board paper analysis, and advanced NEP 2020 competency mapping.

> **Powered by Google Gemini 2.5 Flash** | **13 Weighted Signals** | **10 Years of Data**

## 🚀 What's New in MEGA EDITION

- **20+ YouTube Channels**: Expanded from 4 to 20+ CBSE educators
- **Reddit Community Signals**: r/CBSE, r/IndianStudents analysis
- **Education Blog Scraping**: LearnCBSE, myCBSEguide, Vedantu, Toppr, etc.
- **Pre-Board Paper Analysis**: DPS, KV, DAV, Navodaya patterns
- **NEP 2020 Competency Mapping**: Application, Analysis, Evaluation focus
- **Difficulty Progression Tracking**: Year-over-year difficulty evolution
- **Examiner Behavior Modeling**: Marking scheme preference analysis
- **Mock Paper Generator**: Full exam papers with solutions
- **10-Year Historical Analysis**: 2015-2025 data

## 🧠 Features

### Multi-Signal Analysis (13 Signals)
| Signal | Weight | Description |
|--------|--------|-------------|
| **Blueprint** | 18% | Official 2027 marks distribution & chapter weights |
| **PYQ Frequency** | 16% | Appearance in last 10 years (2015-2025) |
| **YouTube Mentions** | 12% | Consensus among 20+ educators |
| **Gap Bonus** | 12% | Penalty for overdue chapters (absent 2+ years) |
| **Year Trend** | 10% | Recency-weighted trajectory |
| **YouTube Prediction** | 6% | "Sure shot" video signals |
| **Pre-Board Signal** | 6% | DPS, KV, DAV, Navodaya patterns |
| **NCERT Density** | 5% | Questions per page ratio |
| **Blog Consensus** | 4% | Education website predictions |
| **Unit Balance** | 4% | Normalization across units |
| **Difficulty Progression** | 3% | Difficulty evolution analysis |
| **Examiner Preference** | 2% | Marking scheme patterns |
| **Competency Mapping** | 2% | NEP 2020 competency focus |

### Subject Coverage
- **Science (086)**: Physics, Chemistry, Biology with case studies
- **Mathematics (041)**: Standard & Basic with competency-based numericals
- **Social Science (087)**: History, Geography, Civics, Economics with map work

### Smart Question Generation
- Strict adherence to **2027 marking scheme**
- **Case-based questions** (2-3 per paper)
- **Assertion-Reason** questions in every section
- **Map Work** (SST) with 5 guaranteed marks
- **Competency-based** application questions (NEP 2020)
- Prioritizes "gap chapters" (absent for 2+ years)

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Class-X.git
cd Class-X

# Set up Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Get a Gemini API Key (free at Google AI Studio)
export GEMINI_API_KEY="your_api_key_here"
```

## ⚡ Usage

```bash
# Predict all subjects (default 25 questions each)
python main.py

# Predict specific subject(s)
python main.py -s science math

# Generate 30 questions per subject
python main.py -n 30

# MAXIMUM DATA SOURCES (slower but most accurate)
python main.py --max-sources

# Quick mode (essential sources only)
python main.py --quick

# Skip specific sources
python main.py --skip-yt --skip-papers
python main.py --skip-blogs --skip-reddit
python main.py --skip-preboard

# Show signal breakdown per chapter
python main.py --show-signals

# Export results
python main.py --export results.json
python main.py --export-text results.txt
python main.py --export-html results.html

# Generate mock paper with solutions
python main.py --generate-paper
```

## 📂 Project Structure

```
.
├── main.py                    # Entry point with 6-phase pipeline
├── config.py                  # Configuration, weights, 13 signals
├── blueprint.py               # 10-year syllabus & historical data
├── requirements.txt           # Dependencies
│
├── engine/
│   ├── predictor.py           # Gemini prompt engineering for 2027
│   ├── scorer.py              # 13-signal fusion scoring engine
│   └── paper_generator.py     # Mock paper generation with solutions
│
├── scrapers/
│   ├── youtube.py             # 20+ YouTube channel scraper
│   ├── cbse.py                # CBSE SQP/PYQ PDF scraper
│   ├── education_blogs.py     # LearnCBSE, Vedantu, etc. scraper
│   ├── reddit.py              # Reddit community signal extractor
│   └── preboard.py            # DPS/KV/DAV/Navodaya paper scraper
│
├── analyzers/
│   └── pdf.py                 # PDF question extraction
│
├── signals/
│   ├── trend.py               # Gap & trend analysis
│   ├── difficulty.py          # Difficulty progression tracking
│   ├── competency.py          # NEP 2020 competency mapping
│   └── examiner.py            # Examiner behavior modeling
│
├── output/
│   └── formatter.py           # Rich terminal output + exports
│
└── data/                      # Downloaded PDFs & cache
    ├── papers/                # CBSE past papers
    └── preboard/              # Pre-board papers
```

## 🎯 Data Sources

### YouTube Channels (20+)
Shobhit Nirwan, Prashant Kirad, Digraj Singh Rajput, Next Toppers, ExpHub,
Physics Wallah, Vedantu, Unacademy, Dear Sir, Etoos India, Exam Fear,
Magnet Brains, and more...

### Education Blogs
LearnCBSE.in, myCBSEguide, Vedantu, Toppr, BYJU'S, Careers360, Jagran Josh,
Embibe, Successcds

### Community Signals
- Reddit: r/CBSE, r/IndianStudents, r/Indian_Academia
- Pre-board patterns from DPS, KV, DAV, Navodaya schools

### Official CBSE Resources
- Sample Question Papers (SQPs) 2024-2026
- Previous Year Papers (PYQs) 2015-2025
- Marking Schemes with examiner instructions
- Competency-based Question Banks

## 📊 How It Works

1. **Phase 1 - YouTube Scraping**: Extract predictions from 20+ educator channels
2. **Phase 2 - CBSE Papers**: Download & analyze SQPs, PYQs, marking schemes
3. **Phase 3 - Blog Signals**: Scrape education websites for predictions
4. **Phase 4 - Reddit Analysis**: Extract community consensus from discussions
5. **Phase 5 - Pre-Board Papers**: Analyze patterns from top schools
6. **Phase 6 - Multi-Signal Scoring**: Fuse all signals with weighted algorithm
7. **Gemini Prediction**: Generate exam-grade questions with Gemini Flash

## 📝 License

MIT License — use freely for exam preparation!
