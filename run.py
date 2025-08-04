#!/usr/bin/env python3
"""
Website Summarizer CLI - Main entry point.
"""

import sys
from dotenv import load_dotenv
from summarizer import WebsiteSummarizer
from utils import create_argument_parser, save_summary_to_file

# Load environment variables
load_dotenv(override=True)


def main():
    """Main function to run the website summarizer."""
    parser = create_argument_parser()
    args = parser.parse_args()

    summarizer = WebsiteSummarizer()

    if args.verbose:
        print(f"Summarizing: {args.url}")
        print(f"Using model: {summarizer.get_model_type()}")

    summary = summarizer.summarize_url(args.url)

    if args.output:
        save_summary_to_file(summary, args.output)
    else:
        print(summary)


if __name__ == "__main__":
    main()