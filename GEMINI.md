# CBSE Class 10 Board Exam Predictor 2025

This project is a data-driven prediction engine for the CBSE Class 10 Board Exams (2025). It combines official blueprints, historical paper analysis, YouTube prediction signals, and trend analysis, using Gemini 2.5 Flash to generate high-probability questions.

## Project Overview

- **Purpose:** Predict likely questions for CBSE Class 10 (Science, Math, Social Science) based on multiple data signals.
- **Main Technologies:** Python 3, Gemini 2.5 Flash, `yt-dlp`, `pdfplumber`, `BeautifulSoup`, and `Rich`.
- **Architecture:**
    - **Scrapers:** Fetches data from YouTube (prediction videos) and the CBSE Academic website (SQPs, PYQs).
    - **Analyzers:** Processes PDF past papers to extract question frequency, types, and chapter distribution.
    - **Scoring Engine:** A weighted algorithm (`engine/scorer.py`) that combines blueprint weights, PYQ frequency, year-on-year trends, gap analysis (chapters overdue), and social signals (YouTube).
    - **Prediction Engine:** Feeds the highest-scoring chapter data and historical question styles into Gemini to generate original, exam-grade questions.
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

## Project Structure

The project is organized into the following modules:
- `main.py`: Entry point and CLI orchestrator.
- `config.py`: Master configuration, weights, and subject definitions.
- `blueprint.py`: Comprehensive CBSE syllabus and historical appearance data.
- `scrapers/`: Modules for fetching data (`youtube.py`, `cbse.py`, `http.py`).
- `analyzers/`: PDF analysis and question extraction (`pdf.py`).
- `signals/`: Trend analysis and signal computation (`trend.py`).
- `engine/`: Scoring and prediction logic (`scorer.py`, `predictor.py`).
- `output/`: CLI rendering and file export (`formatter.py`).

## Scoring Weights
The prediction logic uses a weighted sum defined in `config.py`:
- `blueprint`: 22%
- `past_papers`: 20%
- `year_trend`: 13%
- `yt_mentions`: 15%
- `gap_bonus`: 10%
- `yt_prediction`: 8%
- `ncert_density`: 7%
- `unit_balance`: 5%
