from abc import ABC, abstractmethod
from typing import Optional, List, Dict

class PromptProcessor(ABC):
    """
    Interface for all prompt processors. Each model type should implement
    its own strategy to format prompts from chat history, user input, and optional system message.
    """

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path
        self.template = self.load_template(template_path) if template_path else None

    def load_template(self, path: str) -> str:
        """Load a prompt template from a file."""
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt template: {path}") from e

    @abstractmethod
    def prepare_prompt(
        self,
        history: List[Dict[str, str]],
        user_input: str,
        system: Optional[str] = None,
        ) -> str:
        """
        Build the full prompt string using message history and the current input.
        Should be implemented by each model-specific processor.

        Args:
            history: List of {"role": ..., "content": ...} messages.
            user_input: The current user message.
            system: Optional system prompt or context.

        Returns:
            Formatted prompt string.
        """
        pass

