from .ollama_prompt import OllamaPromptProcessor
# from prompt_processing.openai_prompt import OpenAIPromptProcessor  # Uncomment if needed
from .base import PromptProcessor

class PromptProcessorFactory:
    @staticmethod
    def create(model_config) -> PromptProcessor:
        """
        Create a PromptProcessor instance based on model_config.
        """
        prompt_processor_name = model_config.get("prompt_processor")

        if prompt_processor_name == "ollama":
            return OllamaPromptProcessor()
        # elif prompt_processor_name == "gemma3_prompt":
        #     return OllamaPromptProcessor()  # Using shared logic for now
        # elif prompt_processor_name == "llama3_prompt":
        #     return OllamaPromptProcessor()  # Also reusing logic
        # # elif prompt_processor_name == "openai":
        #     return OpenAIPromptProcessor()
        else:
            raise ValueError(f"Unknown PromptProcessor: {prompt_processor_name}")
