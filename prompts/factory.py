from .ollama_prompt import OllamaPromptProcessor
# from prompt_processing.openai_prompt import OpenAIPromptProcessor
# Add more imports here as needed

from .base import PromptProcessor

class PromptProcessorFactory:
    @staticmethod
    def load(name: str) -> PromptProcessor:
        """
        Return the appropriate PromptProcessor subclass based on a string key.

        Args:
            name: A string identifier from settings.ini (e.g., "ollama", "gemma3_prompt")

        Returns:
            An instance of a PromptProcessor subclass.
        """
        # if name == "ollama":
        #     return OllamaPromptProcessor()
        # elif name == "openai":
        #     return OpenAIPromptProcessor()
        if name == "gemma3_prompt":
            return OllamaPromptProcessor()  # Can share logic for now
        elif name == "llama3_prompt":
            return OllamaPromptProcessor()  # Also reuse Ollama format
        else:
            raise ValueError(f"No PromptProcessor implementation for: {name}")

