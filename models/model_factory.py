# from models.openai_model import OpenAIModel
from models.ollama_model import OllamaModel
from settings import Settings

class ModelFactory:
    @staticmethod
    def create(name=None):
        settings = Settings()
        model_config = settings.get_model(name)
        provider = model_config.get("provider")

        if provider == "openai":
            return OpenAIModel(model_config)
        elif provider == "ollama":
            return OllamaModel(model_config)

        raise ValueError(f"Unknown provider: {provider}")

