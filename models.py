"""
Model management module for handling different AI models (OpenAI and Ollama).
"""

import os
import sys
from openai import OpenAI


class ModelManager:
    """Manages different AI models (OpenAI and Ollama) for text generation."""

    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.use_openai = self._check_openai_availability()
        self.openai_client = None

        if self.use_openai:
            self.openai_client = OpenAI(api_key=self.api_key)

    def _check_openai_availability(self):
        """Check if OpenAI API key is available and valid."""
        if not self.api_key:
            print("No OpenAI API key found - will use Ollama with Llama 3.2 as fallback")
            return False

        if not self.api_key.startswith("sk-proj-"):
            print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key")
            sys.exit(1)

        if self.api_key.strip() != self.api_key:
            print("An API key was found, but it looks like it might have space or tab characters at the start or end")
            sys.exit(1)

        print("OpenAI API key found and looks good!")
        return True

    def get_model_type(self):
        """Return the current model type being used."""
        return "OpenAI GPT-4o-mini" if self.use_openai else "Ollama Llama 3.2"

    def summarize_with_openai(self, messages):
        """Summarize content using OpenAI's GPT model."""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error summarizing with OpenAI: {str(e)}"

    def summarize_with_ollama(self, messages):
        """Summarize content using Ollama with Llama 3.2."""
        try:
            import ollama

            MODEL = "llama3.2:latest"

            # Check model availability and pull if needed
            if not self._ensure_ollama_model_available(MODEL):
                return f"Error: Could not ensure {MODEL} model is available"

            response = ollama.chat(model=MODEL, messages=messages)
            return response['message']['content']
        except Exception as e:
            return f"Error summarizing with Ollama: {str(e)}"

    def _ensure_ollama_model_available(self, model_name):
        """Ensure the specified Ollama model is available, pulling it if necessary."""
        try:
            import ollama

            models_response = ollama.list()

            # Handle ListResponse object structure
            if hasattr(models_response, 'models'):
                model_names = [model.model for model in models_response.models]
            else:
                # Fallback for dictionary structure
                model_names = [model.get('name', '') for model in models_response.get('models', [])]

            if model_name not in model_names:
                print(f"{model_name} model not found. Attempting to pull it...")
                return self._pull_ollama_model(model_name)

            return True
        except Exception as e:
            print(f"Error listing models: {e}")
            print(f"Attempting to pull {model_name} model directly...")
            return self._pull_ollama_model(model_name)

    def _pull_ollama_model(self, model_name):
        """Pull an Ollama model with progress indication."""
        try:
            import ollama

            for chunk in ollama.pull(model_name, stream=True):
                status = chunk.get('status', 'Unknown')
                print(f"Pulling model: {status}", end='\r')
            print("\nModel pulled successfully!")
            return True
        except Exception as e:
            print(f"\nError pulling model: {e}")
            return False

    def summarize(self, messages):
        """Summarize content using the appropriate model."""
        if self.use_openai:
            return self.summarize_with_openai(messages)
        else:
            return self.summarize_with_ollama(messages)