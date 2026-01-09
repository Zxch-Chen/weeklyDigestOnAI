"""Report generation and output formatting."""
import json
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generates and saves reports in various formats."""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save_markdown(self, content: str, filename: str = None) -> str:
        """
        Save content as a markdown file.
        
        Args:
            content: Markdown content to save
            filename: Optional filename (defaults to timestamped name)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"ai_digest_{timestamp}.md"
        
        filepath = self.output_dir / filename
        filepath.write_text(content, encoding="utf-8")
        
        return str(filepath)

    def save_raw_data(self, data: dict, filename: str = None) -> str:
        """
        Save raw fetched data as JSON.
        
        Args:
            data: Raw data dictionary
            filename: Optional filename
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"raw_data_{timestamp}.json"
        
        filepath = self.output_dir / filename
        filepath.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        
        return str(filepath)

    def generate_header(self, date_range: dict) -> str:
        """Generate report header with metadata."""
        return f"""# 🤖 AI/ML/Robotics Weekly Digest

**Generated**: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}  
**Period**: {date_range.get('start', 'N/A')} to {date_range.get('end', 'N/A')}

---

"""

    def generate_stats_section(self, data: dict) -> str:
        """Generate statistics section."""
        x_count = len(data.get("x_posts", []))
        github_count = len(data.get("github_repos", []))
        arxiv_count = len(data.get("arxiv_papers", []))
        
        return f"""## 📊 Data Summary

| Source | Items Collected |
|--------|-----------------|
| X/Twitter Posts | {x_count} |
| GitHub Repositories | {github_count} |
| arXiv Papers | {arxiv_count} |
| **Total** | **{x_count + github_count + arxiv_count}** |

---

"""

    def format_full_report(self, data: dict, analysis: str) -> str:
        """
        Create a complete formatted report.
        
        Args:
            data: Raw fetched data
            analysis: LLM-generated analysis
            
        Returns:
            Complete markdown report
        """
        header = self.generate_header(data.get("date_range", {}))
        stats = self.generate_stats_section(data)
        
        full_report = f"""{header}{stats}{analysis}

---

## 📝 Methodology

This digest was compiled using:
- **Exa AI** for intelligent web search and content extraction
- **OpenRouter** for LLM analysis and synthesis
- Data sources: X/Twitter, GitHub, arXiv

---

*Generated automatically by RecentNews AI Digest System*
"""
        return full_report
