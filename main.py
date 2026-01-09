"""
RecentNews - AI/ML/Robotics Weekly Digest Generator

Uses Exa AI to fetch relevant content from X/Twitter, GitHub, and arXiv,
then uses an LLM to analyze and compile findings with citations.
"""
import argparse
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown

from src.config import TOPICS
from src.exa_fetcher import ExaFetcher
from src.llm_analyzer import LLMAnalyzer
from src.report_generator import ReportGenerator


console = Console()


def main(
    topics: list[str] = None,
    save_report: bool = True,
    save_raw: bool = False,
    display: bool = True,
):
    """
    Main function to run the AI digest generation.
    
    Args:
        topics: List of topics to search for (defaults to config TOPICS)
        save_report: Whether to save the markdown report
        save_raw: Whether to save raw JSON data
        display: Whether to display the report in console
    """
    topics = topics or TOPICS
    
    console.print(Panel.fit(
        "[bold blue]🤖 AI/ML/Robotics Weekly Digest Generator[/bold blue]\n"
        "[dim]Powered by Exa AI & OpenAI[/dim]",
        border_style="blue"
    ))
    
    # Initialize components
    try:
        fetcher = ExaFetcher()
        analyzer = LLMAnalyzer()
        generator = ReportGenerator()
    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        console.print("[yellow]Please ensure your .env file has EXA_API_KEY and OPENAI_API_KEY set.[/yellow]")
        return

    # Fetch data with progress indication
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Fetch all data
        task = progress.add_task("[cyan]Fetching data from all sources...", total=None)
        data = fetcher.fetch_all(topics)
        progress.update(task, description="[green]✓ Data fetching complete!")
        
        # Analyze with LLM
        progress.update(task, description="[cyan]Analyzing with LLM...")
        analysis = analyzer.analyze_and_compile(data)
        progress.update(task, description="[green]✓ Analysis complete!")
        
        # Generate report
        progress.update(task, description="[cyan]Generating report...")
        full_report = generator.format_full_report(data, analysis)
        progress.update(task, description="[green]✓ Report generated!")

    # Save outputs
    if save_report:
        report_path = generator.save_markdown(full_report)
        console.print(f"[green]📄 Report saved to: {report_path}[/green]")
    
    if save_raw:
        raw_path = generator.save_raw_data(data)
        console.print(f"[green]📊 Raw data saved to: {raw_path}[/green]")

    # Display report
    if display:
        console.print("\n")
        console.print(Panel(
            Markdown(full_report),
            title="[bold]Weekly AI Digest[/bold]",
            border_style="green"
        ))

    return full_report


def quick_fetch(source: str = "all", topics: list[str] = None):
    """
    Quick fetch without LLM analysis.
    
    Args:
        source: 'x', 'github', 'arxiv', or 'all'
        topics: List of topics to search
    """
    topics = topics or TOPICS[:3]
    fetcher = ExaFetcher()
    
    if source == "x":
        return fetcher.fetch_x_posts(topics)
    elif source == "github":
        return fetcher.fetch_github_trending(topics)
    elif source == "arxiv":
        return fetcher.fetch_arxiv_papers(topics)
    else:
        return fetcher.fetch_all(topics)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate AI/ML/Robotics weekly digest"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save the report to file"
    )
    parser.add_argument(
        "--save-raw",
        action="store_true",
        help="Also save raw JSON data"
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Don't display report in console"
    )
    parser.add_argument(
        "--topics",
        nargs="+",
        help="Custom topics to search for"
    )
    
    args = parser.parse_args()
    
    main(
        topics=args.topics,
        save_report=not args.no_save,
        save_raw=args.save_raw,
        display=not args.no_display,
    )
