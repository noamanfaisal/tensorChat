from abc import ABC, abstractmethod
from typing import List, Dict

class BaseChatState(ABC):
    @abstractmethod
    def new_topic(self, model: str, initial_message: str = "") -> None:
        """Start a new topic for the given model."""
        pass

    @abstractmethod
    def add_message(self, role: str, content: str) -> None:
        """Add a message from the user or assistant to the current topic."""
        pass

    @abstractmethod
    def get_messages(self) -> List[Dict[str, str]]:
        """Return all messages in the current topic."""
        pass

    @abstractmethod
    def get_model(self) -> str:
        """Return the model name associated with the current topic."""
        pass

    @abstractmethod
    def save_current_topic(self) -> None:
        """Save the current topic to storage."""
        pass

