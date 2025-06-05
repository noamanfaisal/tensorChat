from abc import ABC, abstractmethod
from typing import Optional, List, Dict

class BasePromptHandler(ABC):
    """
    Abstract base class for prompt handlers.
    """

    @abstractmethod
    def prepare_prompt(self, user_input: str, system_message: Optional[str] = None, 
                       history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Build the prompt string from user input, optional system message, and optional history.

        Args:
            user_input: The current user input.
            system_message: Optional system message or preamble.
            history: Optional list of previous messages in dict format.

        Returns:
            The final prompt string.
        """
        pass

