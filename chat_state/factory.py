from .base_chat_state import BaseChatState
from .ollama_chat_state import OllamaChatState
from .gemma3_chat_state import Gemma3ChatState
from .llama3_chat_state import LLaMA3ChatState
# from .openai_chat_state import OpenAIChatState  # Uncomment when ready

class ChatStateFactory:
    @staticmethod
    def load(name: str, *args, **kwargs) -> BaseChatState:
        """
        Factory to return the correct ChatState subclass based on name from settings.ini.

        Args:
            name (str): The chat_state key (e.g., "ollama", "gemma3_state", etc.)
            *args, **kwargs: Arguments to pass to the ChatState constructor.

        Returns:
            An instance of a ChatState subclass.
        """
        if name == "ollama":
            return OllamaChatState(*args, **kwargs)
        elif name == "gemma3_state":
            return Gemma3ChatState(*args, **kwargs)
        elif name == "llama3_state":
            return LLaMA3ChatState(*args, **kwargs)
        # elif name == "openai":
        #     return OpenAIChatState(*args, **kwargs)
        else:
            raise ValueError(f"No ChatState implementation for: {name}")

