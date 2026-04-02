#!/usr/bin/env python3
"""
main.py — CBSE Class 10 Board Exam Predictor 2027
Ultimate Edition with Maximum Data Sources

Usage:
    python main.py                              # all subjects, 25 questions each
    python main.py -s science math              # specific subjects
    python main.py -n 30                        # 30 questions per subject
    python main.py --force-refresh              # ignore all caches
    python main.py --skip-yt                    # skip YouTube scraping
    python main.py --skip-papers                # skip CBSE PDF scraping
    python main.py --skip-blogs                 # skip education blog scraping
    python main.py --skip-reddit                # skip Reddit scraping
    python main.py --skip-preboard              # skip pre-board paper scraping
    python main.py --scheme                     # print marking scheme hints
    python main.py --export results.json        # export to JSON
    python main.py --export-text results.txt    # export plain text
    python main.py --export-html results.html   # export HTML
    python main.py --show-signals               # show per-chapter signal breakdown
    python main.py --generate-paper             # generate mock paper
    python main.py --max-sources                # enable ALL data sources (slower but better)
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
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
console = Console()

from config import SUBJECTS, SUBJECT_DISPLAY, TARGET_YEAR, CURRENT_SESSION
from output.formatter import (print_banner, print_signal_summary,
                               print_predictions, print_marking_scheme,
                               export_json, export_text)


def parse_args():
    p = argparse.ArgumentParser(
        description=f"CBSE Class 10 Board Exam Predictor {TARGET_YEAR}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("-s", "--subjects", nargs="+", choices=SUBJECTS, default=SUBJECTS, metavar="SUBJECT")
    p.add_argument("-n", "--num-questions", type=int, default=25)
    p.add_argument("--force-refresh", action="store_true", help="Ignore all caches, fetch fresh data")
    
    # Skip flags
    p.add_argument("--skip-yt", action="store_true", help="Skip YouTube scraping")
    p.add_argument("--skip-papers", action="store_true", help="Skip CBSE PDF scraping")
    p.add_argument("--skip-blogs", action="store_true", help="Skip education blog scraping")
    p.add_argument("--skip-reddit", action="store_true", help="Skip Reddit scraping")
    p.add_argument("--skip-preboard", action="store_true", help="Skip pre-board paper analysis")
    
    # Output options
    p.add_argument("--scheme", action="store_true", help="Print marking scheme hints")
    p.add_argument("--show-signals", action="store_true", help="Show per-chapter signal breakdown")
    p.add_argument("--export", metavar="FILE.json", help="Export to JSON")
    p.add_argument("--export-text", metavar="FILE.txt", help="Export plain text")
    p.add_argument("--export-html", metavar="FILE.html", help="Export HTML")
    
    # Advanced options
    p.add_argument("--generate-paper", action="store_true", help="Generate a mock paper")
    p.add_argument("--max-sources", action="store_true", help="Enable ALL data sources")
    p.add_argument("--quick", action="store_true", help="Quick mode - essential sources only")
    
    return p.parse_args()


def main():
    args = parse_args()
    subjects = args.subjects
    force = args.force_refresh
    
    # Quick mode disables slower sources
    if args.quick:
        args.skip_blogs = True
        args.skip_reddit = True
        args.skip_preboard = True
    
    # Max sources enables everything
    if args.max_sources:
        args.skip_blogs = False
        args.skip_reddit = False
        args.skip_preboard = False

    print_banner()
    console.print(f"  [bold cyan]Target Exam:[/bold cyan] CBSE Class X Board {TARGET_YEAR} (Session {CURRENT_SESSION})")
    console.print(f"  [bold cyan]Subjects:[/bold cyan]    {', '.join(SUBJECT_DISPLAY[s] for s in subjects)}")
    console.print(f"  [bold cyan]Questions:[/bold cyan]   {args.num_questions} per subject")
    console.print(f"  [bold cyan]Model:[/bold cyan]       Gemini 2.5 Flash\n")

    # ── Phase 1: YouTube Signals ─────────────────────────────────────────────
    yt_all = {s: {"chapter_scores": {}, "prediction_videos": [], "total_hits": 0} for s in subjects}
    if not args.skip_yt:
        console.print(Rule("[bold yellow]Phase 1/6 — YouTube Prediction Signals[/bold yellow]"))
        from scrapers.youtube import scrape_youtube
        yt_all = scrape_youtube(subjects, force=force)
        for s in subjects:
            console.print(f"  [green]✓[/green] {SUBJECT_DISPLAY[s]}: "
                          f"{yt_all[s]['total_hits']} prediction videos, "
                          f"{len(yt_all[s]['chapter_scores'])} chapters detected")
    else:
        console.print("[dim]Phase 1: YouTube skipped.[/dim]")
    console.print()

    # ── Phase 2: CBSE Papers ─────────────────────────────────────────────────
    pdf_analysis_all = {s: {"chapter_freq": {}, "questions": [], "total_papers": 0} for s in subjects}
    if not args.skip_papers:
        console.print(Rule("[bold yellow]Phase 2/6 — CBSE Past Papers + Analysis[/bold yellow]"))
        from scrapers.cbse import scrape_cbse
        from analyzers.pdf import analyze_all_subjects
        papers = scrape_cbse(subjects, force=force)
        total_pdfs = sum(len(v) for v in papers.values())
        if total_pdfs == 0:
            console.print("  [yellow]! No PDFs found. Drop PDFs manually into data/papers/<subject>/[/yellow]")
        pdf_analysis_all = analyze_all_subjects(papers)
        for s in subjects:
            console.print(f"  [green]✓[/green] {SUBJECT_DISPLAY[s]}: "
                          f"{pdf_analysis_all[s].get('total_papers', 0)} papers, "
                          f"{len(pdf_analysis_all[s].get('questions', []))} questions extracted")
    else:
        console.print("[dim]Phase 2: Paper scraping skipped.[/dim]")
    console.print()

    # ── Phase 3: Education Blogs ─────────────────────────────────────────────
    blog_all = {s: {} for s in subjects}
    if not args.skip_blogs:
        console.print(Rule("[bold yellow]Phase 3/6 — Education Blog Signals[/bold yellow]"))
        try:
            from scrapers.education_blogs import get_blog_signal
            blog_all = get_blog_signal(subjects, force=force)
            for s in subjects:
                chapters_found = len(blog_all.get(s, {}))
                console.print(f"  [green]✓[/green] {SUBJECT_DISPLAY[s]}: {chapters_found} chapters from blogs")
        except Exception as e:
            console.print(f"  [yellow]! Blog scraping failed: {e}[/yellow]")
    else:
        console.print("[dim]Phase 3: Blog scraping skipped.[/dim]")
    console.print()

    # ── Phase 4: Reddit Signals ──────────────────────────────────────────────
    reddit_all = {s: {} for s in subjects}
    if not args.skip_reddit:
        console.print(Rule("[bold yellow]Phase 4/6 — Reddit Community Signals[/bold yellow]"))
        try:
            from scrapers.reddit import get_reddit_signal
            reddit_all = get_reddit_signal(subjects, force=force)
            for s in subjects:
                chapters_found = len(reddit_all.get(s, {}))
                console.print(f"  [green]✓[/green] {SUBJECT_DISPLAY[s]}: {chapters_found} chapters from Reddit")
        except Exception as e:
            console.print(f"  [yellow]! Reddit scraping failed: {e}[/yellow]")
    else:
        console.print("[dim]Phase 4: Reddit scraping skipped.[/dim]")
    console.print()

    # ── Phase 5: Pre-Board Papers ────────────────────────────────────────────
    preboard_all = {s: {} for s in subjects}
    if not args.skip_preboard:
        console.print(Rule("[bold yellow]Phase 5/6 — Pre-Board Paper Analysis[/bold yellow]"))
        try:
            from scrapers.preboard import get_preboard_signal
            preboard_all = get_preboard_signal(subjects, force=force)
            for s in subjects:
                chapters_found = len(preboard_all.get(s, {}))
                console.print(f"  [green]✓[/green] {SUBJECT_DISPLAY[s]}: {chapters_found} chapters from pre-boards")
        except Exception as e:
            console.print(f"  [yellow]! Pre-board scraping failed: {e}[/yellow]")
    else:
        console.print("[dim]Phase 5: Pre-board analysis skipped.[/dim]")
    console.print()

    # ── Phase 6: Trend + Scoring ─────────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 6/6 — Multi-Signal Scoring Engine[/bold yellow]"))
    from signals.trend import get_all_trend_signals
    from engine.scorer import score_all
    
    # Get trend signals
    trend_all = get_all_trend_signals(subjects, pdf_analysis_all)
    
    # Get advanced signals
    difficulty_all = {}
    examiner_all = {}
    competency_all = {}
    
    try:
        from signals.difficulty import get_difficulty_signal
        difficulty_all = get_difficulty_signal(subjects, pdf_analysis_all)
    except Exception as e:
        console.print(f"  [dim]Difficulty signal unavailable: {e}[/dim]")
    
    try:
        from signals.examiner import get_examiner_signal
        examiner_all = get_examiner_signal(subjects, pdf_analysis_all)
    except Exception as e:
        console.print(f"  [dim]Examiner signal unavailable: {e}[/dim]")
    
    try:
        from signals.competency import get_competency_signal
        competency_all = get_competency_signal(subjects, pdf_analysis_all)
    except Exception as e:
        console.print(f"  [dim]Competency signal unavailable: {e}[/dim]")
    
    # Combine blog and reddit signals
    combined_blog = {}
    for s in subjects:
        combined_blog[s] = {}
        for ch, sc in blog_all.get(s, {}).items():
            combined_blog[s][ch] = sc
        for ch, sc in reddit_all.get(s, {}).items():
            combined_blog[s][ch] = combined_blog[s].get(ch, 0) + sc * 0.5
    
    # Final scoring
    chapter_scores = score_all(
        subjects=subjects,
        pdf_analysis=pdf_analysis_all,
        yt_all=yt_all,
        trend_all=trend_all,
        preboard_all=preboard_all,
        blog_all=combined_blog,
        difficulty_all=difficulty_all,
        examiner_all=examiner_all,
        competency_all=competency_all,
    )
    
    for s in subjects:
        top3 = sorted(chapter_scores[s].items(), key=lambda x: -x[1]["score"])[:3]
        console.print(f"  [green]✓[/green] {SUBJECT_DISPLAY[s]}: "
                      + " > ".join(f"{c[:22]}({d['score']:.2f})" for c, d in top3))
    console.print()

    # ── Gemini Prediction ────────────────────────────────────────────────────
    console.print(Rule("[bold magenta]🔮 Gemini Flash Prediction Engine[/bold magenta]"))
    from engine.predictor import generate_predictions
    predictions = generate_predictions(
        subjects=subjects,
        chapter_scores_all=chapter_scores,
        pdf_analysis_all=pdf_analysis_all,
        yt_all=yt_all,
        trend_all=trend_all,
        num_questions=args.num_questions,
    )
    console.print()

    # ── Output ───────────────────────────────────────────────────────────────
    console.print(Rule("[bold cyan]📊 PREDICTIONS[/bold cyan]"))
    for subject in subjects:
        if args.show_signals:
            print_signal_summary(subject, chapter_scores[subject],
                                 yt_all[subject], pdf_analysis_all[subject])
        print_predictions(subject, predictions.get(subject, []))
        if args.scheme:
            print_marking_scheme(subject, predictions.get(subject, []))

    # Exports
    if args.export:
        export_json(predictions, chapter_scores, args.export)
    if args.export_text:
        export_text(predictions, args.export_text)
    if args.export_html:
        try:
            from output.html_export import export_html
            export_html(predictions, chapter_scores, args.export_html)
        except ImportError:
            # Fallback: basic HTML export
            html_content = "<html><body><h1>CBSE Predictions</h1>"
            for subj, qs in predictions.items():
                html_content += f"<h2>{subj}</h2><ol>"
                for q in qs:
                    html_content += f"<li><b>[{q.get('marks')}M]</b> {q.get('question', '')}</li>"
                html_content += "</ol>"
            html_content += "</body></html>"
            Path(args.export_html).write_text(html_content)
            console.print(f"  [green]HTML export: {args.export_html}[/green]")

    # Generate mock paper if requested
    if args.generate_paper:
        console.print(Rule("[bold green]📝 Mock Paper Generation[/bold green]"))
        from engine.paper_generator import generate_paper, save_paper, paper_to_text
        for subject in subjects:
            console.print(f"  Generating {SUBJECT_DISPLAY[subject]} paper...", end=" ")
            paper = generate_paper(subject, chapter_scores[subject])
            if "error" not in paper:
                filepath = save_paper(paper, subject)
                console.print(f"[green]✓[/green] Saved to {filepath}")
            else:
                console.print(f"[red]✗[/red] {paper.get('error', 'Unknown error')}")

    # Summary stats
    total_questions = sum(len(predictions.get(s, [])) for s in subjects)
    high_conf = sum(1 for s in subjects for q in predictions.get(s, []) if q.get("confidence") == "High")
    
    console.print()
    console.print(Panel(
        f"[bold green]✅ Prediction Complete![/bold green]\n\n"
        f"Total Questions: [cyan]{total_questions}[/cyan]\n"
        f"High Confidence: [green]{high_conf}[/green]\n"
        f"Target Exam: CBSE Board {TARGET_YEAR}\n\n"
        f"[dim]Best of luck! 🎯[/dim]",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
