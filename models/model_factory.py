# from models.openai_model import OpenAIModel
from .ollama_model import OllamaModel

class ModelFactory:

    @staticmethod
    def create(model_config):
        provider = model_config.get("provider")

        if provider == "openai":
            pass
            # return OpenAIModel(model_config)
        elif provider == "ollama":
            return OllamaModel(model_config)
        raise ValueError(f"Unknown provider: {provider}")
