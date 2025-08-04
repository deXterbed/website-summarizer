"""
Web scraping module for extracting content from websites.
"""

import requests
from bs4 import BeautifulSoup


class WebsiteScraper:
    """Handles website scraping and content extraction."""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

    def scrape_website(self, url):
        """Scrape a website and return a Website object."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else "No title found"

            # Remove irrelevant elements
            for element in soup.find_all(["script", "style", "img", "input"]):
                element.decompose()

            # Extract text content
            if soup.body:
                text = soup.body.get_text(separator="\n", strip=True)
            else:
                text = soup.get_text(separator="\n", strip=True)

            return Website(url, title, text)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL {url}: {e}")


class Website:
    """Represents a scraped website with its content."""

    def __init__(self, url, title, text):
        self.url = url
        self.title = title
        self.text = text

    def __str__(self):
        return f"Website(url='{self.url}', title='{self.title}', text_length={len(self.text)})"

    def __repr__(self):
        return self.__str__()