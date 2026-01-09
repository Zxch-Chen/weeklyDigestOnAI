"""LLM-powered analysis and compilation of fetched data."""
from openai import OpenAI

from .config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL


class LLMAnalyzer:
    """Analyzes and compiles findings using an LLM via OpenRouter."""

    def __init__(self, model: str = None):
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not set. Please add it to your .env file.")
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )
        self.model = model or DEFAULT_MODEL

    def analyze_and_compile(self, data: dict) -> str:
        """
        Analyze all fetched data and compile a comprehensive report.
        
        Args:
            data: Dictionary containing x_posts, github_repos, and arxiv_papers
            
        Returns:
            Compiled markdown report with analysis, citations, and links
        """
        # Prepare context for the LLM
        context = self._prepare_context(data)
        
        system_prompt = """You are an expert AI/ML research analyst. Your job is to analyze 
recent developments in AI, LLMs, and robotics, and compile a comprehensive weekly digest.

Your report should:
1. Identify the most significant developments and trends
2. Group related items together thematically
3. Provide insightful analysis on why these developments matter
4. Include proper citations with URLs for all sources
5. Highlight any breakthrough research or viral projects
6. Note connections between different developments
7. Provide a brief executive summary at the top

Format the report in clean Markdown with:
- Executive Summary section
- Key Themes/Trends section
- Detailed breakdown by category (Papers, GitHub Projects, Social Discussion)
- Each item should have a linked citation
- A "What to Watch" section for emerging trends

Be concise but thorough. Focus on signal over noise."""

        user_prompt = f"""Please analyze the following data collected over the past week and compile 
a comprehensive AI/ML/Robotics weekly digest with full citations and links.

Date Range: {data.get('date_range', {}).get('start', 'N/A')} to {data.get('date_range', {}).get('end', 'N/A')}

{context}

Please compile a comprehensive report with analysis, insights, and proper citations (include URLs)."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating analysis: {e}"

    def summarize_single_source(self, source_type: str, items: list[dict]) -> str:
        """
        Generate a summary for a single source type.
        
        Args:
            source_type: Type of source (x_posts, github_repos, arxiv_papers)
            items: List of items from that source
            
        Returns:
            Summary markdown text
        """
        if not items:
            return f"No {source_type} data available."

        context = self._format_items(items)
        
        source_names = {
            "x_posts": "X/Twitter Posts",
            "github_repos": "GitHub Repositories",
            "arxiv_papers": "arXiv Papers"
        }
        
        prompt = f"""Summarize the following {source_names.get(source_type, source_type)} 
about AI/LLM/Robotics. Highlight the most important/trending items and include URLs as citations.

{context}

Provide a concise summary with key takeaways and links to the most notable items."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error summarizing {source_type}: {e}"

    def _prepare_context(self, data: dict) -> str:
        """Prepare all data as context for the LLM."""
        sections = []
        
        # X/Twitter Posts
        if data.get("x_posts"):
            sections.append("## X/Twitter Posts\n")
            sections.append(self._format_items(data["x_posts"]))
        
        # GitHub Repos
        if data.get("github_repos"):
            sections.append("\n## GitHub Repositories\n")
            sections.append(self._format_items(data["github_repos"]))
        
        # arXiv Papers
        if data.get("arxiv_papers"):
            sections.append("\n## arXiv Papers\n")
            sections.append(self._format_items(data["arxiv_papers"]))
        
        return "\n".join(sections)

    def _format_items(self, items: list[dict]) -> str:
        """Format a list of items for LLM context."""
        formatted = []
        
        for i, item in enumerate(items, 1):
            entry = f"""
### Item {i}
- **Source**: {item.get('source', 'Unknown')}
- **Topic**: {item.get('topic', 'General')}
- **Title**: {item.get('title', 'No title')}
- **URL**: {item.get('url', 'No URL')}
- **Date**: {item.get('published_date', 'Unknown date')}
- **Content**: {item.get('text', item.get('abstract', item.get('description', 'No content')))}
"""
            if item.get('highlights'):
                entry += f"- **Key Highlights**: {' | '.join(item['highlights'][:3])}\n"
            
            formatted.append(entry)
        
        return "\n".join(formatted)
