"""
Main summarizer module that orchestrates the website summarization process.
"""

from models import ModelManager
from scraper import WebsiteScraper
from prompts import PromptBuilder


class WebsiteSummarizer:
    """Main class for website summarization functionality."""

    def __init__(self):
        self.model_manager = ModelManager()
        self.scraper = WebsiteScraper()

    def summarize_url(self, url):
        """Summarize the content of a website."""
        try:
            website = self.scraper.scrape_website(url)
            messages = PromptBuilder.build_messages(website)
            return self.model_manager.summarize(messages)
        except Exception as e:
            return f"Error summarizing {url}: {str(e)}"

    def summarize_with_custom_prompt(self, url, system_prompt=None, user_prompt=None):
        """Summarize with custom prompts."""
        try:
            website = self.scraper.scrape_website(url)

            if system_prompt and user_prompt:
                messages = PromptBuilder.build_custom_messages(system_prompt, user_prompt)
            else:
                messages = PromptBuilder.build_messages(website)

            return self.model_manager.summarize(messages)
        except Exception as e:
            return f"Error summarizing {url}: {str(e)}"

    def get_model_type(self):
        """Get the current model type being used."""
        return self.model_manager.get_model_type()

    def is_using_openai(self):
        """Check if OpenAI is being used."""
        return self.model_manager.use_openai