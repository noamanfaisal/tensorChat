from .base import BaseChatState
from .ollama import OllamaChatState
from .gemma3_ollama import Gemma3OllamaChatState
from .llama3_ollama import LLaMa3OllamaChatState
# from .openai_chat_state import OpenAIChatState  # Uncomment when ready

class ChatStateFactory:

    @staticmethod
    def create(model_config, *args, **kwargs) -> BaseChatState:
        """
        Create a ChatState instance based on model_config.
        """
        chat_state_name = model_config.get("chat_state")

        if chat_state_name == "ollama":
            return OllamaChatState(*args, **kwargs)
        # elif chat_state_name == "gemma3_state":
        #     return Gemma3OllamaChatState(*args, **kwargs)
        # elif chat_state_name == "llama3_state":
        #     return LLaMa3OllamaChatState(*args, **kwargs)
        else:
          raise ValueError(f"Unknown ChatState: {chat_state_name}")
