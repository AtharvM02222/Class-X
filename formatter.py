"""output/formatter.py — rich terminal output + JSON/text export."""
import json, sys
from datetime import datetime
from pathlib import Path
from collections import Counter
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.progress import BarColumn, Progress
from rich.rule import Rule
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import REPORTS_DIR

console = Console(highlight=False)

CONF_STYLE  = {"High": "bold green", "Medium": "bold yellow", "Low": "bold red"}
TYPE_STYLE  = {"MCQ":"dim white","SA-I":"cyan","SA-II":"blue","LA":"bold magenta",
               "CASE":"bold yellow","DIAGRAM":"bold cyan","MAP":"bold green","?":"dim"}
MARKS_ICON  = {1:"●", 2:"●●", 3:"●●●", 4:"●●●●", 5:"●●●●●"}

def _bar(score: float, width: int = 12) -> str:
    filled = int(round(score * width))
    return "█" * filled + "░" * (width - filled)

def print_banner():
    console.print()
    console.print(Panel(
        "[bold cyan]CBSE Class 10 Board Exam Predictor 2025[/bold cyan]\n"
        "[dim]Signals: Blueprint · Past Papers · Year Trends · YouTubers (Shobhit Nirwan · Prashant Dhawan · Digraj Singh Rajput) · Gemini Pro[/dim]",
        box=box.DOUBLE_EDGE, border_style="cyan", padding=(0, 6),
    ))
    console.print()

def print_signal_summary(subject: str, chapter_scores: dict, yt_data: dict, pdf_data: dict):
    console.print(Rule(f"[bold white] Signal Summary — {subject.replace('_',' ').title()} [/bold white]", style="blue"))
    top = sorted(chapter_scores.items(), key=lambda x: -x[1]["score"])[:8]
    t = Table(box=box.SIMPLE, show_header=True, header_style="bold dim", padding=(0,1))
    t.add_column("Chapter",    style="italic", min_width=35)
    t.add_column("Score",      width=14)
    t.add_column("Conf",       width=7)
    t.add_column("Blueprint",  width=10)
    t.add_column("Papers",     width=10)
    t.add_column("YT",         width=10)
    t.add_column("Gap",        width=8)
    for chap, data in top:
        c = data["components"]
        bar = f"[{'green' if data['score']>0.65 else 'yellow' if data['score']>0.4 else 'red'}]{_bar(data['score'])}[/] {data['score']:.3f}"
        conf_s = f"[{CONF_STYLE.get(data['confidence'],'white')}]{data['confidence']}[/]"
        t.add_row(
            chap[:38], bar, conf_s,
            _bar(c["blueprint"],8),
            _bar(c["past_papers"],8),
            _bar(c["yt_signal"],8),
            f"[green]{c['gap_bonus']:.2f}[/]" if c["gap_bonus"] > 0.3 else f"{c['gap_bonus']:.2f}",
        )
    console.print(t)
    total_yt = yt_data.get("total_hits", 0)
    total_pdf = pdf_data.get("total_papers", 0)
    console.print(f"  [dim]YT prediction videos matched: {total_yt}  |  PDFs analyzed: {total_pdf}[/dim]\n")

def print_predictions(subject: str, questions: list[dict]):
    s_display = subject.replace("_", " ").title()
    console.print(Rule(f"[bold white on blue]  {s_display} — Predicted Questions  [/bold white on blue]", style="blue"))
    console.print()

    if not questions:
        console.print("  [red]No predictions generated.[/red]\n")
        return

    t = Table(box=box.ROUNDED, show_header=True, header_style="bold white",
              border_style="blue", expand=True, padding=(0, 1), show_lines=True)
    t.add_column("#",        width=3,  no_wrap=True, style="dim")
    t.add_column("M",        width=3,  no_wrap=True)
    t.add_column("Type",     width=7,  no_wrap=True)
    t.add_column("Conf",     width=7,  no_wrap=True)
    t.add_column("Score",    width=7,  no_wrap=True)
    t.add_column("Chapter",  width=30, style="italic cyan")
    t.add_column("Question", min_width=45)
    t.add_column("Reason",   min_width=28, style="dim")

    for q in questions:
        rank   = str(q.get("rank", "?"))
        marks  = q.get("marks", "?")
        qtype  = q.get("type", "?")
        conf   = q.get("confidence", "?")
        score  = q.get("composite_score", 0.0)
        chap   = q.get("chapter", "?")[:30]
        ques   = q.get("question", "?")
        reason = q.get("reason", "")[:80]

        marks_str = f"[bold]{MARKS_ICON.get(marks, str(marks))}[/bold]" if isinstance(marks, int) else str(marks)
        type_str  = f"[{TYPE_STYLE.get(qtype,'white')}]{qtype}[/]"
        conf_str  = f"[{CONF_STYLE.get(conf,'white')}]{conf}[/]"
        score_str = f"[{'green' if score>0.65 else 'yellow' if score>0.4 else 'red'}]{score:.3f}[/]"

        t.add_row(rank, marks_str, type_str, conf_str, score_str, chap, ques, reason)

    console.print(t)

    # stats footer
    conf_c  = Counter(q.get("confidence") for q in questions)
    marks_c = Counter(q.get("marks") for q in questions)
    console.print(
        f"  [dim]Confidence: [green]{conf_c.get('High',0)} High[/green] "
        f"[yellow]{conf_c.get('Medium',0)} Med[/yellow] "
        f"[red]{conf_c.get('Low',0)} Low[/red]  "
        f"| Marks: {' '.join(f'{k}M×{v}' for k,v in sorted(marks_c.items()) if k)}[/dim]\n"
    )

def print_marking_scheme(subject: str, questions: list[dict]):
    """Print marking scheme for all LA questions."""
    la_qs = [q for q in questions if q.get("marks", 0) >= 4 and q.get("scheme")]
    if not la_qs: return
    console.print(Rule(f"[bold yellow] Marking Scheme Hints — {subject.replace('_',' ').title()} [/bold yellow]", style="yellow"))
    for q in la_qs:
        console.print(f"\n  [bold]Q{q['rank']}. ({q['marks']}M) {q.get('chapter','?')}[/bold]")
        console.print(f"  [dim]{q['question'][:120]}...[/dim]")
        console.print(f"  [yellow]Scheme:[/yellow] {q.get('scheme','')}")
    console.print()

def export_json(predictions: dict, chapter_scores: dict, filepath: str):
    data = {
        "generated_at": datetime.now().isoformat(),
        "tool": "CBSE Class 10 Board Predictor 2025",
        "signals": ["blueprint","past_papers","year_trend","youtube","gemini_pro"],
        "chapter_scores": {
            subj: {ch: {"score": d["score"], "confidence": d["confidence"], "rank": d["rank"]}
                   for ch, d in scores.items()}
            for subj, scores in chapter_scores.items()
        },
        "predictions": predictions,
    }
    p = Path(filepath)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    console.print(f"\n  [green]Exported to {p}[/green]")

def export_text(predictions: dict, filepath: str):
    lines = ["CBSE Class 10 Board Exam Predictor 2025", "=" * 60, ""]
    for subject, questions in predictions.items():
        lines.append(f"\n{'='*60}")
        lines.append(f"  {subject.replace('_',' ').upper()}")
        lines.append(f"{'='*60}")
        for q in questions:
            lines.append(f"\nQ{q['rank']}. [{q.get('marks','?')}M | {q.get('type','?')} | {q.get('confidence','?')}]")
            lines.append(f"Chapter: {q.get('chapter','?')}")
            lines.append(f"{q.get('question','?')}")
            if q.get("scheme"):
                lines.append(f"Scheme: {q['scheme']}")
            lines.append(f"Reason: {q.get('reason','')}")
            lines.append("-" * 50)
    Path(filepath).write_text("\n".join(lines), encoding="utf-8")
    console.print(f"  [green]Text export: {filepath}[/green]")
