from .base import BaseChatState
from .ollama import OllamaChatState
from .gemma3_ollama import Gemma3OllamaChatState
from .llama3_ollama import  LLaMa3OllamaChatState
# from .openai_chat_state import OpenAIChatState  # Uncomment when ready

class ChatStateFactory:
    @staticmethod
    def load(name: str, *args, **kwargs) -> BaseChatState:
        if name == "ollama":
            return OllamaChatState(*args, **kwargs)
        elif name == "gemma3_state":
            return Gemma3OllamaChatState(*args, **kwargs)
        elif name == "llama3_state":
            return LLaMa3OllamaChatState(*args, **kwargs)
        else:
            raise ValueError(f"No ChatState implementation for: {name}")

