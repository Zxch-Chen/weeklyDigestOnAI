# 🤖 RecentNews - AI/ML/Robotics Weekly Digest

An intelligent news aggregator that uses **Exa AI** to fetch the most relevant content about AI, LLMs, and Robotics from X/Twitter, GitHub, and arXiv, then uses an **LLM** to analyze and compile findings with citations.

## Features

- 🐦 **X/Twitter Posts**: Fetches trending discussions and announcements
- 🐙 **GitHub Repositories**: Finds trending repos with star activity
- 📄 **arXiv Papers**: Collects recent research papers on AI/ML/Robotics
- 🧠 **LLM Analysis**: Uses GPT-4 to analyze, synthesize, and provide insights
- 📊 **Compiled Reports**: Generates markdown reports with proper citations and links

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
EXA_API_KEY=your_exa_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your API keys:
- **Exa AI**: https://exa.ai (sign up for API access)
- **OpenRouter**: https://openrouter.ai/keys

### 3. Run the Digest Generator

```bash
python main.py
```

## Usage Options

```bash
# Generate full report (default)
python main.py

# Generate without saving to file
python main.py --no-save

# Also save raw JSON data
python main.py --save-raw

# Don't display in console (useful for automation)
python main.py --no-display

# Custom topics
python main.py --topics "GPT-5" "Claude" "Gemini" "robotics"
```

## Programmatic Usage

```python
from main import main, quick_fetch

# Generate full report
report = main(topics=["LLM", "robotics"], save_report=True)

# Quick fetch without LLM analysis
x_posts = quick_fetch(source="x", topics=["AI"])
github_repos = quick_fetch(source="github", topics=["LLM"])
arxiv_papers = quick_fetch(source="arxiv", topics=["robotics"])
all_data = quick_fetch(source="all")
```

## Project Structure

```
RecentNews/
├── main.py              # Entry point and CLI
├── requirements.txt     # Python dependencies
├── .env                 # API keys (create from .env.example)
├── .env.example         # Example environment file
├── README.md            # This file
├── reports/             # Generated reports (auto-created)
└── src/
    ├── __init__.py
    ├── config.py        # Configuration settings
    ├── exa_fetcher.py   # Exa AI data fetching
    ├── llm_analyzer.py  # LLM analysis and synthesis
    └── report_generator.py  # Report formatting and saving
```

## Configuration

Edit `src/config.py` to customize:

```python
# Number of results per search
SEARCH_SETTINGS = {
    "num_results": 10,
    "days_back": 7,  # Weekly delta window
}

# Topics to search for
TOPICS = [
    "LLM",
    "large language model",
    "AI artificial intelligence",
    "robotics",
    # Add your own topics...
]
```

## Output Example

Reports are saved to the `reports/` directory in Markdown format:

```markdown
# 🤖 AI/ML/Robotics Weekly Digest

**Generated**: January 9, 2026 at 03:45 PM
**Period**: 2026-01-02 to 2026-01-09

## 📊 Data Summary
| Source | Items Collected |
|--------|-----------------|
| X/Twitter Posts | 15 |
| GitHub Repositories | 12 |
| arXiv Papers | 18 |

## Executive Summary
...

## Key Trends
...
```

## Dependencies

- `exa_py` - Exa AI Python SDK
- `openai` - OpenAI-compatible client (used for OpenRouter)
- `python-dotenv` - Environment variable management
- `rich` - Beautiful terminal output

## Supported Models (via OpenRouter)

You can change the model in `src/config.py`. Popular options:

### Free Models (No Credits Required)
- **`xiaomi/mimo-v2-flash:free`** (default) - 262k context, best for agentic tools. Turn off reasoning mode for fast agentic capabilities, use reasoning flag for reasoning tasks.
- **`nvidia/nemotron-3-nano-30b-a3b:free`** - 256k context, good general purpose model
- **`mistralai/devstral-2512:free`** - 262k context, best for agentic coding
- **`arcee-ai/trinity-mini:free`** - Best for long-term efficient reasoning with robust function calling and multi-step agent workflows
- **`nvidia/nemotron-nano-12b-v2-vl:free`** - 128k context, supports image input with language output
- **`deepseek/deepseek-r1-0528:free`** - 164k context, strong reasoning capabilities

### Paid Models (Require Credits)
- `anthropic/claude-sonnet-4` - Latest Claude model, great for analysis
- `openai/gpt-4o` - OpenAI's GPT-4 Optimized
- `google/gemini-2.0-flash-001` - Google's latest Gemini model
- `meta-llama/llama-3-70b-instruct` - Meta's Llama 3 70B

See all models at: https://openrouter.ai/models

## 🚀 Automated Weekly Digests with GitHub Actions

Set up automatic weekly email digests using GitHub Actions!

### Setup Instructions

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Digest Generator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Configure Repository Secrets**
   Go to your GitHub repo → Settings → Secrets and variables → Actions
   
   Add these secrets:
   - `EXA_API_KEY`: Your Exa AI API key
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `EMAIL_USERNAME`: Your Gmail address (for sending emails)
   - `EMAIL_PASSWORD`: Your Gmail app password (not regular password!)
   - `EMAIL_RECIPIENT`: Email address to receive digests

3. **Set up Gmail App Password**
   - Go to Google Account settings
   - Enable 2-factor authentication
   - Generate an "App Password" for GitHub Actions
   - Use this app password as `EMAIL_PASSWORD`

4. **Customize Schedule** (Optional)
   Edit `.github/workflows/weekly-digest.yml`:
   ```yaml
   schedule:
     - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
   ```
   Use [crontab.guru](https://crontab.guru) to customize timing.

### Features

- ✅ **Weekly Automation**: Runs every Monday automatically
- ✅ **Email Delivery**: Sends formatted HTML emails with the digest
- ✅ **Artifact Storage**: Saves reports for 30 days in GitHub
- ✅ **Manual Trigger**: Can run on-demand via GitHub Actions tab
- ✅ **Error Handling**: Workflow fails gracefully if APIs are down

### Workflow Details

The GitHub Actions workflow:
1. Sets up Python environment
2. Installs dependencies
3. Runs the digest generator
4. Formats the report for email
5. Sends HTML email with full digest
6. Uploads artifacts for download

### Cost

- **GitHub Actions**: Free for public repos, 2000 minutes/month for private
- **APIs**: Exa AI and OpenRouter free tiers
- **Email**: Uses Gmail (free)

---

## License

MIT
