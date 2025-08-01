# Website Summarizer CLI

A command-line tool that uses OpenAI's GPT model to automatically summarize website content. The tool scrapes web pages, extracts meaningful text content, and generates concise markdown summaries.

## Features

- **CLI Interface**: Easy-to-use command-line interface with argument parsing
- **Web Scraping**: Automatically extracts and cleans website content
- **AI-Powered Summaries**: Uses OpenAI's GPT-4o-mini model for intelligent summarization
- **Flexible Output**: Print to console or save to file
- **Error Handling**: Robust error handling for network issues and API problems
- **Verbose Mode**: Optional detailed output for debugging

## Installation

### Prerequisites

- Python 3.7 or higher
- OpenAI API key

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:

   ```bash
   pip install openai requests beautifulsoup4 python-dotenv
   ```

3. **Set up your OpenAI API key**:

   Create a `.env` file in the project directory:

   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

   Replace `your_api_key_here` with your actual OpenAI API key.

## Usage

### Basic Usage

Summarize a website and print the result to console:

```bash
python run.py https://anthropic.com
```

### Save Summary to File

```bash
python run.py https://example.com --output summary.md
```

### Verbose Mode

Get detailed output including the URL being processed:

```bash
python run.py https://example.com --verbose
```

### Help

View all available options:

```bash
python run.py --help
```

## Command Line Arguments

| Argument    | Short | Description                                    |
| ----------- | ----- | ---------------------------------------------- |
| `url`       | -     | The URL of the website to summarize (required) |
| `--output`  | `-o`  | Output file to save the summary                |
| `--verbose` | `-v`  | Enable verbose output                          |
| `--help`    | `-h`  | Show help message                              |

## Examples

### Summarize a tech company website

```bash
python run.py https://openai.com
```

### Save summary to a markdown file

```bash
python run.py https://github.com --output github_summary.md
```

### Verbose output for debugging

```bash
python run.py https://example.com --verbose --output debug_summary.md
```

## How It Works

1. **Web Scraping**: The tool fetches the webpage using requests with a realistic user agent
2. **Content Extraction**: BeautifulSoup parses the HTML and extracts text content while removing scripts, styles, images, and form inputs
3. **AI Processing**: The cleaned text is sent to OpenAI's GPT-4o-mini model with a system prompt to generate a summary
4. **Output**: The AI-generated markdown summary is returned to the user

## Error Handling

The tool handles various error scenarios:

- **Missing API Key**: Exits with error message if OpenAI API key is not found
- **Invalid API Key**: Validates API key format and exits if invalid
- **Network Errors**: Handles connection timeouts and HTTP errors
- **File I/O Errors**: Gracefully handles file writing errors

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### API Key Format

The tool expects an API key that starts with `sk-proj-`. Make sure you're using the correct API key format.

## Troubleshooting

### Common Issues

1. **"No API key was found"**

   - Ensure you have a `.env` file with your OpenAI API key
   - Check that the API key is properly formatted

2. **"API key doesn't start with sk-proj-"**

   - Verify you're using the correct OpenAI API key
   - Check for any extra spaces or characters

3. **Network errors**

   - Check your internet connection
   - Verify the URL is accessible
   - Some websites may block automated requests

4. **Rate limiting**
   - OpenAI has rate limits on API calls
   - Wait a moment and try again

## Dependencies

- `openai`: OpenAI API client
- `requests`: HTTP library for web scraping
- `beautifulsoup4`: HTML parsing library
- `python-dotenv`: Environment variable management

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## Security Notes

- Never commit your `.env` file with API keys
- The `.gitignore` file is configured to exclude sensitive files
- API keys are loaded from environment variables for security
