#!/usr/bin/env python3
"""
Test module for the website summarizer.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv(override=True)

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import ModelManager
from scraper import WebsiteScraper, Website
from prompts import PromptBuilder
from summarizer import WebsiteSummarizer
from utils import validate_url, format_summary, save_summary_to_file
from config import ERROR_MESSAGES


class TestWebsiteScraper(unittest.TestCase):
    """Test cases for WebsiteScraper."""

    def setUp(self):
        self.scraper = WebsiteScraper()

    @patch('requests.get')
    def test_scrape_website_success(self, mock_get):
        """Test successful website scraping."""
        # Mock response
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
            <head><title>Test Website</title></head>
            <body>
                <h1>Welcome</h1>
                <p>This is a test website.</p>
                <script>alert('test');</script>
            </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        website = self.scraper.scrape_website('https://example.com')

        self.assertEqual(website.url, 'https://example.com')
        self.assertEqual(website.title, 'Test Website')
        self.assertIn('Welcome', website.text)
        self.assertIn('This is a test website', website.text)
        self.assertNotIn('alert', website.text)  # Script should be removed

    @patch('requests.get')
    def test_scrape_website_failure(self, mock_get):
        """Test website scraping failure."""
        mock_get.side_effect = Exception('Connection failed')

        with self.assertRaises(Exception):
            self.scraper.scrape_website('https://invalid-url.com')


class TestWebsite(unittest.TestCase):
    """Test cases for Website class."""

    def test_website_creation(self):
        """Test Website object creation."""
        website = Website('https://example.com', 'Test Title', 'Test content')

        self.assertEqual(website.url, 'https://example.com')
        self.assertEqual(website.title, 'Test Title')
        self.assertEqual(website.text, 'Test content')

    def test_website_string_representation(self):
        """Test Website string representation."""
        website = Website('https://example.com', 'Test Title', 'Test content')
        str_repr = str(website)

        self.assertIn('https://example.com', str_repr)
        self.assertIn('Test Title', str_repr)
        self.assertIn('text_length=12', str_repr)  # "Test content" has 12 characters


class TestPromptBuilder(unittest.TestCase):
    """Test cases for PromptBuilder."""

    def setUp(self):
        self.website = Website('https://example.com', 'Test Website', 'This is test content.')

    def test_build_messages(self):
        """Test message building."""
        messages = PromptBuilder.build_messages(self.website)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[1]['role'], 'user')
        self.assertIn('Test Website', messages[1]['content'])
        self.assertIn('This is test content', messages[1]['content'])

    def test_build_custom_messages(self):
        """Test custom message building."""
        system_prompt = "You are a helpful assistant."
        user_prompt = "Summarize this content."

        messages = PromptBuilder.build_custom_messages(system_prompt, user_prompt)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['content'], system_prompt)
        self.assertEqual(messages[1]['content'], user_prompt)

    def test_get_default_system_prompt(self):
        """Test getting default system prompt."""
        prompt = PromptBuilder.get_default_system_prompt()
        self.assertIsInstance(prompt, str)
        self.assertIn('assistant', prompt)


class TestModelManager(unittest.TestCase):
    """Test cases for ModelManager."""

    @patch.dict(os.environ, {'OPENAI_API_KEY': ''})
    def test_no_openai_key(self):
        """Test behavior when no OpenAI API key is available."""
        manager = ModelManager()
        self.assertFalse(manager.use_openai)
        self.assertEqual(manager.get_model_type(), "Ollama Llama 3.2")

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'sk-proj-test-key'})
    def test_valid_openai_key(self):
        """Test behavior with valid OpenAI API key."""
        manager = ModelManager()
        self.assertTrue(manager.use_openai)
        self.assertEqual(manager.get_model_type(), "OpenAI GPT-4o-mini")


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            'https://example.com',
            'http://test.org',
            'https://www.google.com/path'
        ]

        for url in valid_urls:
            self.assertTrue(validate_url(url))

    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            'example.com',
            'ftp://example.com',
            'not-a-url',
            ''
        ]

        for url in invalid_urls:
            self.assertFalse(validate_url(url))

    def test_format_summary(self):
        """Test summary formatting."""
        long_summary = "This is a very long summary that exceeds the maximum length limit."

        # Test with length limit
        formatted = format_summary(long_summary, max_length=20)
        self.assertEqual(len(formatted), 23)  # 20 chars + "..."
        self.assertTrue(formatted.endswith("..."))

        # Test without length limit
        formatted = format_summary(long_summary)
        self.assertEqual(formatted, long_summary)

    def test_save_summary_to_file(self):
        """Test saving summary to file."""
        summary = "Test summary content"
        test_file = "test_summary.txt"

        try:
            # Test successful save
            result = save_summary_to_file(summary, test_file)
            self.assertTrue(result)

            # Verify file was created
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertEqual(content, summary)

        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)


class TestWebsiteSummarizer(unittest.TestCase):
    """Test cases for WebsiteSummarizer."""

    def setUp(self):
        self.summarizer = WebsiteSummarizer()

    @patch('scraper.WebsiteScraper.scrape_website')
    @patch('models.ModelManager.summarize')
    def test_summarize_url_success(self, mock_summarize, mock_scrape):
        """Test successful URL summarization."""
        # Mock website
        mock_website = Website('https://example.com', 'Test', 'Content')
        mock_scrape.return_value = mock_website

        # Mock summary
        mock_summarize.return_value = "Test summary"

        result = self.summarizer.summarize_url('https://example.com')

        self.assertEqual(result, "Test summary")
        mock_scrape.assert_called_once_with('https://example.com')
        mock_summarize.assert_called_once()

    @patch('scraper.WebsiteScraper.scrape_website')
    def test_summarize_url_failure(self, mock_scrape):
        """Test URL summarization failure."""
        mock_scrape.side_effect = Exception("Scraping failed")

        result = self.summarizer.summarize_url('https://example.com')

        self.assertIn("Error summarizing", result)
        self.assertIn("Scraping failed", result)


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestWebsiteScraper,
        TestWebsite,
        TestPromptBuilder,
        TestModelManager,
        TestUtils,
        TestWebsiteSummarizer
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)