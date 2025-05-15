from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

class BaseChatState(ABC):
    @abstractmethod
    def new_topic(self, model: str, initial_message: str = "") -> None:
        pass

    @abstractmethod
    def add_message(self, role: str, content: str) -> None:
        pass

    @abstractmethod
    def get_messages(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def get_model(self) -> str:
        pass

    @abstractmethod
    def save_current_topic(self) -> None:
        pass

    # 🔽 Optional: Context handling (token list for Ollama, message history for OpenAI)
    def get_context(self) -> Optional[Any]:
        """Return the in-memory context (tokens or messages)."""
        return None

    def set_context(self, context: Any) -> None:
        """Set the in-memory context (tokens or messages)."""
        pass
