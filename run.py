import os
import requests
import argparse
import sys
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check if we should use OpenAI or fallback to Ollama
use_openai = False
if api_key:
    if not api_key.startswith("sk-proj-"):
        print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
        sys.exit(1)
    elif api_key.strip() != api_key:
        print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
        sys.exit(1)
    else:
        print("OpenAI API key found and looks good!")
        use_openai = True
else:
    print("No OpenAI API key found - will use Ollama with Llama 3.2 as fallback")

# Initialize OpenAI client if API key is available
openai_client = None
if use_openai:
    openai_client = OpenAI(api_key=api_key)

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL {url}: {e}")

        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"

        # Remove script, style, img, and input elements
        for irrelevant in soup.find_all(["script", "style", "img", "input"]):
            irrelevant.decompose()

        # Get text content
        if soup.body:
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = soup.get_text(separator="\n", strip=True)

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def summarize_with_openai(website):
    """
    Summarize the content of a website using OpenAI's GPT model.

    Args:
        website (Website): The Website object to summarize

    Returns:
        str: A markdown summary of the website content
    """
    try:
        response = openai_client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages_for(website)
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing with OpenAI: {str(e)}"

def summarize_with_ollama(website):
    """
    Summarize the content of a website using Ollama with Llama 3.2.

    Args:
        website (Website): The Website object to summarize

    Returns:
        str: A markdown summary of the website content
    """
    try:
        import ollama

        MODEL = "llama3.2:latest"

        # Check if llama3.2 model is available, if not try to pull it
        try:
            models_response = ollama.list()
            # Handle ListResponse object structure
            if hasattr(models_response, 'models'):
                model_names = [model.model for model in models_response.models]
            else:
                # Fallback for dictionary structure
                model_names = [model.get('name', '') for model in models_response.get('models', [])]

            if MODEL not in model_names:
                print(f"{MODEL} model not found. Attempting to pull it...")
                try:
                    for chunk in ollama.pull(MODEL, stream=True):
                        status = chunk.get('status', 'Unknown')
                        print(f"Pulling model: {status}", end='\r')
                    print("\nModel pulled successfully!")
                except Exception as pull_error:
                    print(f"\nError pulling model: {pull_error}")
                    return f"Error: Could not pull {MODEL} model. Please ensure Ollama is running and you have internet access."
        except Exception as list_error:
            print(f"Error listing models: {list_error}")
            # Try to pull the model anyway, as it might be a connection issue
            print(f"Attempting to pull {MODEL} model directly...")
            try:
                for chunk in ollama.pull(MODEL, stream=True):
                    status = chunk.get('status', 'Unknown')
                    print(f"Pulling model: {status}", end='\r')
                print("\nModel pulled successfully!")
            except Exception as pull_error:
                print(f"\nError pulling model: {pull_error}")
                return f"Error: Could not connect to Ollama. Please ensure Ollama is running on localhost:11434"

        response = ollama.chat(model=MODEL, messages=messages_for(website))

        return response['message']['content']
    except Exception as e:
        return f"Error summarizing with Ollama: {str(e)}"

def summarize(url):
    """
    Summarize the content of a website using either OpenAI or Ollama.

    Args:
        url (str): The URL of the website to summarize

    Returns:
        str: A markdown summary of the website content
    """
    try:
        website = Website(url)

        if use_openai:
            return summarize_with_openai(website)
        else:
            return summarize_with_ollama(website)
    except Exception as e:
        return f"Error summarizing {url}: {str(e)}"

def main():
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

    args = parser.parse_args()

    if args.verbose:
        model_type = "OpenAI GPT-4o-mini" if use_openai else "Ollama Llama 3.2"
        print(f"Summarizing: {args.url}")
        print(f"Using model: {model_type}")

    summary = summarize(args.url)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"Summary saved to: {args.output}")
        except Exception as e:
            print(f"Error saving to {args.output}: {e}")
            print("\nSummary:")
            print(summary)
    else:
        print(summary)

if __name__ == "__main__":
    main()