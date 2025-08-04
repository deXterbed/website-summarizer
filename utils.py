"""
Utility functions for the website summarizer.
"""

import argparse


def create_argument_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Summarize website content using OpenAI's GPT model or Ollama with Llama 3.2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py https://anthropic.com
  python run.py https://example.com --output summary.md

Note: If no OpenAI API key is found, the script will automatically use Ollama with Llama 3.2.
Make sure Ollama is running on localhost:11434 for local model usage.
        """
    )

    parser.add_argument(
        "url",
        help="The URL of the website to summarize"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file to save the summary (default: print to stdout)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    return parser


def save_summary_to_file(summary, output_file):
    """Save summary to a file with error handling."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"Summary saved to: {output_file}")
        return True
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")
        print("\nSummary:")
        print(summary)
        return False


def validate_url(url):
    """Basic URL validation."""
    if not url.startswith(('http://', 'https://')):
        return False
    return True


def format_summary(summary, max_length=None):
    """Format summary with optional length limit."""
    if max_length and len(summary) > max_length:
        return summary[:max_length] + "..."
    return summary