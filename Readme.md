# CBSE Class 10 Board Exam Predictor 2026

An elite AI-powered exam intelligence system that predicts the **CBSE Class 10 Board Exam 2026** questions by fusing 15 years of historical data, official blueprint weights, YouTube educator signals, and year-over-year trend analysis.

> **Powered by Google Gemini 2.5 Flash**

## 🚀 Features

- **Multi-Signal Analysis**: Combines 5 independent data streams:
  - 📘 **Official Blueprint**: 2026 marks distribution & chapter weights.
  - 📄 **Past Paper Analysis**: 15 years (2010–2024) of question frequency data.
  - 📈 **Trend Signals**: Gap analysis (overdue chapters) & alternation rules.
  - 📺 **YouTube Intelligence**: Scrapes predictions from top educators (Shobhit Nirwan, Digraj Singh Rajput, Next Toppers, ExpHub).
  - 🤖 **Gemini 2.5 Flash**: Generates exam-grade questions with strict adherence to CBSE style.

- **Subject Coverage**:
  - **Science (086)**: Physics, Chemistry, Biology
  - **Mathematics (041)**: Standard & Basic
  - **Social Science (087)**: History, Geography, Civics, Economics

- **Smart Question Generation**:
  - Strict adherence to 2026 marking scheme.
  - Includes **Case-based**, **Assertion-Reason**, and **Map Work** (SST) questions.
  - Prioritizes "gap chapters" (absent for 2+ years).

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Class-X.git
    cd Class-X
    ```

2.  **Set up Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Get a Gemini API Key**:
    - Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    - Export it:
      ```bash
      export GEMINI_API_KEY="your_api_key_here"
      ```

## ⚡ Usage

Run the main predictor script:

```bash
# Predict all subjects (default 25 questions each)
python main.py

# Predict specific subject(s)
python main.py -s science math

# Generate 30 questions per subject
python main.py -n 30

# Skip YouTube scraping (faster)
python main.py --skip-yt

# Export results to JSON
python main.py --export results.json
```

## 🧠 Intelligence Engine

The system uses a weighted scoring model to rank chapters:

| Signal | Weight | Description |
|---|---|---|
| **Blueprint** | 22% | Official marks allocation |
| **Past Frequency** | 20% | Appearance in last 8-15 years |
| **YouTube Mentions** | 15% | Consensus among top educators |
| **Year Trend** | 13% | Recency-weighted trajectory |
| **Gap Bonus** | 10% | Penalty for overdue chapters |
| **YouTube Prediction** | 8% | "Sure shot" video signals |
| **NCERT Density** | 7% | Questions per page ratio |
| **Unit Balance** | 5% | Normalization across units |

## 📂 Project Structure

```
.
├── main.py              # Entry point
├── config.py            # Configuration & Weights
├── blueprint.py         # CBSE Syllabus & Historical Data
├── engine/
│   ├── predictor.py     # Gemini Prompt Engineering
│   └── scorer.py        # Signal Fusion Logic
├── scrapers/
│   ├── youtube.py       # YouTube Data Scraper
│   └── cbse.py          # PDF Scraper
├── signals/
│   └── trend.py         # Gap & Trend Analysis
└── output/
    └── formatter.py     # Rich Terminal Output
```

## 📝 License

MIT License.
