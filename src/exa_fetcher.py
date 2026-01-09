"""Exa AI data fetcher for tweets, GitHub repos, and arXiv papers."""
from datetime import datetime, timedelta
from typing import Optional
from exa_py import Exa

from .config import EXA_API_KEY, SEARCH_SETTINGS


class ExaFetcher:
    """Fetches data from various sources using Exa AI."""

    def __init__(self):
        if not EXA_API_KEY:
            raise ValueError("EXA_API_KEY not set. Please add it to your .env file.")
        self.client = Exa(api_key=EXA_API_KEY)
        self.num_results = SEARCH_SETTINGS["num_results"]
        self.days_back = SEARCH_SETTINGS["days_back"]

    def _get_date_range(self) -> tuple[str, str]:
        """Get date range for the past week."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.days_back)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    def fetch_x_posts(self, topics: list[str]) -> list[dict]:
        """
        Fetch relevant X (Twitter) posts about AI/LLM/Robotics.
        
        Args:
            topics: List of topics to search for
            
        Returns:
            List of tweet data with url, title, text, author, and date
        """
        start_date, end_date = self._get_date_range()
        all_posts = []

        for topic in topics[:3]:  # Limit to top 3 topics to avoid rate limits
            query = f"{topic} AI breakthrough OR announcement site:twitter.com OR site:x.com"
            
            try:
                results = self.client.search_and_contents(
                    query=query,
                    num_results=self.num_results,
                    start_published_date=start_date,
                    end_published_date=end_date,
                    text=True,
                    highlights=True,
                )

                for result in results.results:
                    all_posts.append({
                        "source": "X/Twitter",
                        "topic": topic,
                        "url": result.url,
                        "title": result.title or "No title",
                        "text": result.text[:500] if result.text else "",
                        "highlights": result.highlights if hasattr(result, 'highlights') else [],
                        "published_date": result.published_date if hasattr(result, 'published_date') else None,
                        "author": result.author if hasattr(result, 'author') else "Unknown",
                    })
            except Exception as e:
                print(f"Error fetching X posts for '{topic}': {e}")

        return all_posts

    def fetch_github_trending(self, topics: list[str]) -> list[dict]:
        """
        Fetch trending GitHub repositories related to AI/LLM/Robotics.
        
        Args:
            topics: List of topics to search for
            
        Returns:
            List of repo data with url, name, description, stars info
        """
        start_date, end_date = self._get_date_range()
        all_repos = []

        for topic in topics[:3]:
            # Search for GitHub repos with recent activity
            query = f"{topic} repository stars site:github.com"
            
            try:
                results = self.client.search_and_contents(
                    query=query,
                    num_results=self.num_results,
                    start_published_date=start_date,
                    end_published_date=end_date,
                    text=True,
                    highlights=True,
                )

                for result in results.results:
                    # Extract repo info from URL
                    url = result.url
                    repo_name = self._extract_repo_name(url)
                    
                    all_repos.append({
                        "source": "GitHub",
                        "topic": topic,
                        "url": url,
                        "name": repo_name,
                        "title": result.title or repo_name,
                        "description": result.text[:500] if result.text else "",
                        "highlights": result.highlights if hasattr(result, 'highlights') else [],
                        "published_date": result.published_date if hasattr(result, 'published_date') else None,
                    })
            except Exception as e:
                print(f"Error fetching GitHub repos for '{topic}': {e}")

        return all_repos

    def fetch_arxiv_papers(self, topics: list[str]) -> list[dict]:
        """
        Fetch recent arXiv papers on LLM, AI, and Robotics.
        
        Args:
            topics: List of topics to search for
            
        Returns:
            List of paper data with url, title, abstract, authors, and date
        """
        start_date, end_date = self._get_date_range()
        all_papers = []

        for topic in topics[:4]:  # More topics for papers
            query = f"{topic} research paper site:arxiv.org"
            
            try:
                results = self.client.search_and_contents(
                    query=query,
                    num_results=self.num_results,
                    start_published_date=start_date,
                    end_published_date=end_date,
                    text=True,
                    highlights=True,
                )

                for result in results.results:
                    all_papers.append({
                        "source": "arXiv",
                        "topic": topic,
                        "url": result.url,
                        "title": result.title or "Untitled Paper",
                        "abstract": result.text[:800] if result.text else "",
                        "highlights": result.highlights if hasattr(result, 'highlights') else [],
                        "published_date": result.published_date if hasattr(result, 'published_date') else None,
                        "author": result.author if hasattr(result, 'author') else "Unknown",
                    })
            except Exception as e:
                print(f"Error fetching arXiv papers for '{topic}': {e}")

        return all_papers

    def fetch_all(self, topics: list[str]) -> dict:
        """
        Fetch all data sources.
        
        Args:
            topics: List of topics to search for
            
        Returns:
            Dictionary containing x_posts, github_repos, and arxiv_papers
        """
        print("Fetching X/Twitter posts...")
        x_posts = self.fetch_x_posts(topics)
        
        print("Fetching GitHub repositories...")
        github_repos = self.fetch_github_trending(topics)
        
        print("Fetching arXiv papers...")
        arxiv_papers = self.fetch_arxiv_papers(topics)

        return {
            "x_posts": x_posts,
            "github_repos": github_repos,
            "arxiv_papers": arxiv_papers,
            "fetch_date": datetime.now().isoformat(),
            "date_range": {
                "start": self._get_date_range()[0],
                "end": self._get_date_range()[1],
            }
        }

    @staticmethod
    def _extract_repo_name(url: str) -> str:
        """Extract repository name from GitHub URL."""
        try:
            parts = url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
            return url
        except:
            return url
