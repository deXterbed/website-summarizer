# Website Summarizer CLI

A command-line tool that uses OpenAI's GPT model or Ollama with Llama 3.2 to automatically summarize website content. The tool scrapes web pages, extracts meaningful text content, and generates concise markdown summaries.

## Features

- **CLI Interface**: Easy-to-use command-line interface with argument parsing
- **Web Scraping**: Automatically extracts and cleans website content
- **AI-Powered Summaries**: Uses OpenAI's GPT-4o-mini model or Ollama with Llama 3.2 for intelligent summarization
- **Dual Model Support**: Automatically falls back to local Llama 3.2 if OpenAI API key is not available
- **Modular Architecture**: Well-organized, testable, and maintainable codebase
- **Flexible Output**: Print to console or save to file
- **Error Handling**: Robust error handling for network issues and API problems
- **Verbose Mode**: Optional detailed output for debugging
- **Comprehensive Testing**: Full test suite with 15+ test cases

## Installation

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (optional - will use Ollama if not provided)
- Ollama (for local model usage)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:

   ```bash
   pip install openai requests beautifulsoup4 python-dotenv ollama
   ```

3. **Set up your OpenAI API key** (optional):

   Create a `.env` file in the project directory:

   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

   Replace `your_api_key_here` with your actual OpenAI API key.

   **Note**: If no API key is provided, the tool will automatically use Ollama with Llama 3.2.

4. **Install Ollama** (for local model usage):

   Visit [ollama.ai](https://ollama.ai) to download and install Ollama.

   The tool will automatically pull the Llama 3.2 model on first use.

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

Get detailed output including the URL being processed and which model is being used:

```bash
python run.py https://example.com --verbose
```

### Help

View all available options:

```bash
python run.py --help
```

## Model Selection

The tool automatically selects the appropriate model:

- **OpenAI GPT-4o-mini**: Used when a valid OpenAI API key is found in the `.env` file
- **Ollama Llama 3.2**: Used as fallback when no OpenAI API key is available

The tool will automatically download the Llama 3.2 model on first use if it's not already available.

## Ollama Support

### What is Ollama?

Ollama is an open-source tool that allows you to run large language models locally on your machine. This provides several benefits:

- **Privacy**: No data sent to external servers
- **Offline Usage**: Works without internet connection (after model download)
- **Cost-Free**: No API costs for model usage
- **Customizable**: Easy to switch between different models

### Ollama Setup

1. **Install Ollama**:

   - Visit [ollama.ai](https://ollama.ai)
   - Download and install for your platform
   - Start the Ollama service

2. **Model Management**:

   - The tool automatically pulls `llama3.2:latest` on first use
   - Models are stored locally and reused
   - No additional configuration required

3. **Usage Examples**:

   ```bash
   # Without OpenAI API key - uses Ollama automatically
   python run.py https://example.com --verbose

   # Check which model is being used
   python run.py https://example.com --verbose
   # Output: Using model: Ollama Llama 3.2
   ```

### Ollama vs OpenAI

| Feature           | OpenAI              | Ollama              |
| ----------------- | ------------------- | ------------------- |
| **Setup**         | API key required    | Local installation  |
| **Cost**          | Pay per request     | Free                |
| **Privacy**       | Data sent to OpenAI | Local processing    |
| **Speed**         | Fast (cloud)        | Depends on hardware |
| **Offline**       | Requires internet   | Works offline       |
| **Model Quality** | Latest GPT models   | Various open models |

## Project Structure

The project is organized into modular components for maintainability and testability:

```
website-summarizer/
├── run.py                 # Main CLI entry point
├── models.py              # AI model management (OpenAI/Ollama)
├── scraper.py             # Web scraping functionality
├── prompts.py             # Prompt building and management
├── summarizer.py          # Main orchestrator class
├── utils.py               # Utility functions and helpers
├── config.py              # Configuration settings
├── test_summarizer.py     # Comprehensive test suite
├── requirements.txt       # Dependencies
└── README.md             # This file
```

### Module Overview

- **`models.py`**: Handles all AI model interactions (OpenAI and Ollama)
- **`scraper.py`**: Dedicated to web scraping and content extraction
- **`prompts.py`**: Manages prompt construction for AI models
- **`summarizer.py`**: Main orchestrator that coordinates all components
- **`utils.py`**: Common utility functions (URL validation, file operations)
- **`config.py`**: Centralized configuration and constants

## Advanced Usage

### Using Individual Components

```python
from summarizer import WebsiteSummarizer
from scraper import WebsiteScraper
from models import ModelManager
from prompts import PromptBuilder

# Use the main summarizer
summarizer = WebsiteSummarizer()
summary = summarizer.summarize_url("https://example.com")

# Use individual components
scraper = WebsiteScraper()
website = scraper.scrape_website("https://example.com")

model_manager = ModelManager()
messages = PromptBuilder.build_messages(website)
summary = model_manager.summarize(messages)
```

### Custom Prompts

```python
from summarizer import WebsiteSummarizer

summarizer = WebsiteSummarizer()

# Use custom prompts
system_prompt = "You are a technical writer. Provide a detailed technical summary."
user_prompt = "Analyze this website and provide a technical overview."

summary = summarizer.summarize_with_custom_prompt(
    "https://example.com",
    system_prompt=system_prompt,
    user_prompt=user_prompt
)
```

### Model Information

```python
from summarizer import WebsiteSummarizer

summarizer = WebsiteSummarizer()

print(f"Using OpenAI: {summarizer.is_using_openai()}")
print(f"Model type: {summarizer.get_model_type()}")
```

## Testing

Run the comprehensive test suite:

```bash
python test_summarizer.py
```

The test suite includes:

- **15+ test cases** covering all major functionality
- **Mocked external dependencies** for reliable testing
- **Error handling tests** for robust validation
- **Component isolation** for modular testing

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

### Using local model (no API key required)

```bash
# Remove or comment out OPENAI_API_KEY from .env file
python run.py https://example.com --verbose
```

### Compare OpenAI vs Ollama

```bash
# With OpenAI API key
python run.py https://example.com --verbose
# Output: Using model: OpenAI GPT-4o-mini

# Without OpenAI API key
mv .env .env.backup
python run.py https://example.com --verbose
# Output: Using model: Ollama Llama 3.2
```

## Troubleshooting

### Ollama Issues

1. **Ollama not running**:

   ```bash
   # Start Ollama service
   ollama serve
   ```

2. **Model not found**:

   ```bash
   # Pull the model manually
   ollama pull llama3.2:latest
   ```

3. **Connection issues**:
   - Ensure Ollama is running on `localhost:11434`
   - Check firewall settings
   - Verify internet connection for model download

### OpenAI Issues

1. **Invalid API key**:

   - Ensure key starts with `sk-proj-`
   - Remove any whitespace from the key
   - Check key validity in OpenAI dashboard

2. **Rate limiting**:
   - Wait before making additional requests
   - Consider using Ollama as fallback

### General Issues

1. **URL not accessible**:

   - Check URL validity
   - Ensure website is publicly accessible
   - Try with `--verbose` for detailed error messages

2. **File save errors**:
   - Check write permissions
   - Ensure directory exists
   - Verify disk space

## Contributing

The modular architecture makes it easy to contribute:

1. **Add new models**: Extend `models.py` with new model support
2. **Improve scraping**: Enhance `scraper.py` with better content extraction
3. **Custom prompts**: Modify `prompts.py` for different use cases
4. **Add tests**: Extend `test_summarizer.py` with new test cases

## License

This project is open source and available under the MIT License.
