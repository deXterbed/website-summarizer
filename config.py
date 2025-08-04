"""
Configuration settings for the website summarizer.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Model Configuration
OPENAI_MODEL = "gpt-4o-mini"
OLLAMA_MODEL = "llama3.2:latest"

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OLLAMA_HOST = "http://localhost:11434"

# Web Scraping Configuration
REQUEST_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

# Elements to remove during scraping
ELEMENTS_TO_REMOVE = ["script", "style", "img", "input", "nav", "footer", "header"]

# Default prompts
DEFAULT_SYSTEM_PROMPT = """You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."""

DEFAULT_USER_PROMPT_TEMPLATE = """You are looking at a website titled {title}
The contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.

{content}"""

# Output Configuration
DEFAULT_ENCODING = 'utf-8'
MAX_SUMMARY_LENGTH = 10000  # characters

# Error Messages
ERROR_MESSAGES = {
    'openai_key_invalid': "An API key was found, but it doesn't start sk-proj-; please check you're using the right key",
    'openai_key_whitespace': "An API key was found, but it looks like it might have space or tab characters at the start or end",
    'ollama_connection': "Could not connect to Ollama. Please ensure Ollama is running on localhost:11434",
    'model_pull_failed': "Could not pull {model} model. Please ensure Ollama is running and you have internet access",
    'url_fetch_failed': "Failed to fetch URL {url}: {error}",
    'file_save_failed': "Error saving to {file}: {error}"
}