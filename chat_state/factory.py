from typing import Type
from .base_chat_state import BaseChatState
from .ollama_chat_state import OllamaChatState
# from .openai_chat_state import OpenAIChatState  # You’ll define this as a minimal subclass

def load_chat_state(provider: str, *args, **kwargs) -> BaseChatState:
    """
    Factory to return the correct ChatState subclass based on provider name.
    
    Args:
        provider (str): The model provider (e.g., "ollama", "openai").
        *args, **kwargs: Arguments to pass to the ChatState constructor.

    Returns:
        An instance of a ChatState subclass.
    """
    if provider == "ollama":
        return OllamaChatState(*args, **kwargs)
    elif provider == "openai":
        pass
        # return OpenAIChatState(*args, **kwargs)
    else:
        raise ValueError(f"No ChatState implementation for provider: {provider}")

