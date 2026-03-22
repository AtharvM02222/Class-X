# CBSE Class 10 Board Exam Predictor 2025

This project is a data-driven prediction engine for the CBSE Class 10 Board Exams (2025). It combines official blueprints, historical paper analysis, YouTube prediction signals, and trend analysis, using Gemini 1.5 Pro to generate high-probability questions.

## Project Overview

- **Purpose:** Predict likely questions for CBSE Class 10 (Science, Math, Social Science) based on multiple data signals.
- **Main Technologies:** Python 3, Gemini 1.5 Pro, `yt-dlp`, `pdfplumber`, `BeautifulSoup`, and `Rich`.
- **Architecture:**
    - **Scrapers:** Fetches data from YouTube (prediction videos) and the CBSE Academic website (SQPs, PYQs).
    - **Analyzers:** Processes PDF past papers to extract question frequency, types, and chapter distribution.
    - **Scoring Engine:** A weighted algorithm (`scorer.py`) that combines blueprint weights, PYQ frequency, year-on-year trends, gap analysis (chapters overdue), and social signals (YouTube).
    - **Prediction Engine:** Feeds the highest-scoring chapter data and historical question styles into Gemini 1.5 Pro to generate original, exam-grade questions.
    - **Output:** Provides a rich CLI summary and exports results to JSON or Text.

## Building and Running

### Prerequisites
- Python 3.10+
- A Google Gemini API Key ([get one here](https://aistudio.google.com/app/apikey))

### Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set your API Key:**
   ```bash
   export GEMINI_API_KEY=your_key_here
   ```

### Running the Predictor
- **Default (all subjects, 25 questions each):**
  ```bash
  python main.py
  ```
- **Specific Subjects:**
  ```bash
  python main.py -s science math
  ```
- **Custom Question Count:**
  ```bash
  python main.py -n 30
  ```
- **Export Results:**
  ```bash
  python main.py --export results.json --export-text results.txt
  ```
- **Force Refresh Caches:**
  ```bash
  python main.py --force-refresh
  ```

## Project Structure & Conventions

### Directory Layout
The project currently has all files in the root directory, although the internal code assumes a nested structure. Key files include:
- `config.py`: Master configuration, weights, and subject definitions.
- `blueprint.py`: Comprehensive CBSE syllabus, unit weights, and 8-year historical appearance data.
- `main.py`: Entry point and CLI orchestrator.
- `youtube.py`, `cbse.py`, `http.py`: Data ingestion from external sources.
- `pdf.py`: PDF text and question extraction.
- `trend.py`, `scorer.py`: Signal processing and chapter ranking.
- `predictor.py`: Gemini-powered generation logic.
- `formatter.py`: CLI rendering and file export.

### Development Note
The codebase contains `sys.path` modifications and imports (e.g., `from scrapers.youtube import ...`) that suggest a nested directory structure was intended (e.g., `scrapers/`, `engine/`, `analyzers/`). Currently, all files are located in the project root.

### Scoring Weights
The prediction logic uses a weighted sum defined in `config.py`:
- `blueprint`: 22%
- `pyq_frequency`: 20%
- `year_trend`: 13%
- `yt_mentions`: 15%
- `gap_bonus`: 10% (Bonus for chapters that haven't appeared recently)
