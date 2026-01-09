"""Configuration settings for the news aggregator."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
EXA_API_KEY = os.getenv("EXA_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter settings
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "xiaomi/mimo-v2-flash:free"  # Free model: 262k context, great for agentic tools

# Search settings
SEARCH_SETTINGS = {
    "num_results": 10,
    "days_back": 7,  # For weekly delta calculations
}

# Topics to search for
TOPICS = [
    "LLM",
    "large language model",
    "AI artificial intelligence",
    "robotics",
    "machine learning",
    "neural network",
    "GPT",
    "transformer model",
]
