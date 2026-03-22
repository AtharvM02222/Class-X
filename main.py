#!/usr/bin/env python3
"""
main.py — CBSE Class 10 Board Exam Predictor 2025
Combines: CBSE Blueprint + Past Papers + Year Trend + YouTubers + Gemini Pro

Usage:
    python main.py                              # all subjects, 25 questions each
    python main.py -s science math              # specific subjects
    python main.py -n 30                        # 30 questions per subject
    python main.py --force-refresh              # ignore all caches
    python main.py --skip-yt                    # skip YouTube scraping
    python main.py --skip-papers                # skip CBSE PDF scraping
    python main.py --scheme                     # print marking scheme hints
    python main.py --export results.json        # export to JSON
    python main.py --export-text results.txt    # export plain text
    python main.py --show-signals               # show per-chapter signal breakdown
"""

import argparse, os, sys
from pathlib import Path

if "--help" not in sys.argv and "-h" not in sys.argv:
    if not os.getenv("GEMINI_API_KEY"):
        print("\n  ERROR: GEMINI_API_KEY not set.")
        print("  Run:   export GEMINI_API_KEY=your_key_here")
        print("  Free key: https://aistudio.google.com/app/apikey\n")
        sys.exit(1)

from rich.console import Console
from rich.rule import Rule
console = Console()

from config import SUBJECTS, SUBJECT_DISPLAY
from output.formatter import (print_banner, print_signal_summary,
                               print_predictions, print_marking_scheme,
                               export_json, export_text)


def parse_args():
    p = argparse.ArgumentParser(
        description="CBSE Class 10 Board Exam Predictor 2025",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("-s", "--subjects", nargs="+", choices=SUBJECTS, default=SUBJECTS, metavar="SUBJECT")
    p.add_argument("-n", "--num-questions", type=int, default=25)
    p.add_argument("--force-refresh", action="store_true")
    p.add_argument("--skip-yt",     action="store_true")
    p.add_argument("--skip-papers", action="store_true")
    p.add_argument("--scheme",      action="store_true")
    p.add_argument("--show-signals",action="store_true")
    p.add_argument("--export",      metavar="FILE.json")
    p.add_argument("--export-text", metavar="FILE.txt")
    return p.parse_args()


def main():
    args    = parse_args()
    subjects= args.subjects
    force   = args.force_refresh

    print_banner()
    console.print(f"  Subjects : [cyan]{', '.join(SUBJECT_DISPLAY[s] for s in subjects)}[/cyan]")
    console.print(f"  Questions: [cyan]{args.num_questions} per subject[/cyan]")
    console.print(f"  Model    : [cyan]Gemini 1.5 Pro[/cyan]\n")

    # ── 1. YouTube ────────────────────────────────────────────────────────
    yt_all = {s: {"chapter_scores": {}, "prediction_videos": [], "total_hits": 0} for s in subjects}
    if not args.skip_yt:
        console.print(Rule("[bold yellow]1 / 4  YouTube Prediction Signals[/bold yellow]"))
        from scrapers.youtube import scrape_youtube
        yt_all = scrape_youtube(subjects, force=force)
        for s in subjects:
            console.print(f"  [green]v[/green] {SUBJECT_DISPLAY[s]}: "
                          f"{yt_all[s]['total_hits']} prediction videos, "
                          f"{len(yt_all[s]['chapter_scores'])} chapters detected")
    else:
        console.print("[dim]YouTube skipped.[/dim]")
    console.print()

    # ── 2. CBSE papers ───────────────────────────────────────────────────
    pdf_analysis_all = {s: {"chapter_freq":{}, "questions":[], "total_papers":0} for s in subjects}
    if not args.skip_papers:
        console.print(Rule("[bold yellow]2 / 4  CBSE Past Papers + Analysis[/bold yellow]"))
        from scrapers.cbse import scrape_cbse
        from analyzers.pdf import analyze_all_subjects
        papers = scrape_cbse(subjects, force=force)
        total_pdfs = sum(len(v) for v in papers.values())
        if total_pdfs == 0:
            console.print("  [yellow]! No PDFs found. Drop PDFs manually into data/papers/<subject>/[/yellow]")
        pdf_analysis_all = analyze_all_subjects(papers)
        for s in subjects:
            console.print(f"  [green]v[/green] {SUBJECT_DISPLAY[s]}: "
                          f"{pdf_analysis_all[s].get('total_papers',0)} papers, "
                          f"{len(pdf_analysis_all[s].get('questions',[]))} questions extracted")
    else:
        console.print("[dim]Paper scraping skipped.[/dim]")
    console.print()

    # ── 3. Trend + scoring ───────────────────────────────────────────────
    console.print(Rule("[bold yellow]3 / 4  Trend Analysis + Signal Scoring[/bold yellow]"))
    from signals.trend import get_all_trend_signals
    from engine.scorer import score_all
    trend_all      = get_all_trend_signals(subjects, pdf_analysis_all)
    chapter_scores = score_all(subjects, pdf_analysis_all, yt_all, trend_all)
    for s in subjects:
        top3 = sorted(chapter_scores[s].items(), key=lambda x: -x[1]["score"])[:3]
        console.print(f"  [green]v[/green] {SUBJECT_DISPLAY[s]}: "
                      + " > ".join(f"{c[:22]}({d['score']:.2f})" for c, d in top3))
    console.print()

    # ── 4. Gemini ────────────────────────────────────────────────────────
    console.print(Rule("[bold yellow]4 / 4  Gemini Pro Prediction Engine[/bold yellow]"))
    from engine.predictor import generate_predictions
    predictions = generate_predictions(
        subjects           = subjects,
        chapter_scores_all = chapter_scores,
        pdf_analysis_all   = pdf_analysis_all,
        yt_all             = yt_all,
        trend_all          = trend_all,
        num_questions      = args.num_questions,
    )
    console.print()

    # ── Output ────────────────────────────────────────────────────────────
    console.print(Rule("[bold cyan] PREDICTIONS [/bold cyan]"))
    for subject in subjects:
        if args.show_signals:
            print_signal_summary(subject, chapter_scores[subject],
                                 yt_all[subject], pdf_analysis_all[subject])
        print_predictions(subject, predictions.get(subject, []))
        if args.scheme:
            print_marking_scheme(subject, predictions.get(subject, []))

    if args.export:
        export_json(predictions, chapter_scores, args.export)
    if args.export_text:
        export_text(predictions, args.export_text)

    console.print("\n  [bold green]Done! Best of luck 🎯[/bold green]\n")


if __name__ == "__main__":
    main()
