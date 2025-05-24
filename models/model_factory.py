# from models.openai_model import OpenAIModel
from .ollama_model import OllamaModel

class ModelFactory:

    @staticmethod
    def create(model_config):
        # 
        model = model_config.get("model")

        if model == "openai":
            pass
            # return OpenAIModel(model_config)
        elif model == "ollama":
            return OllamaModel(model_config)
        raise ValueError(f"Unknown model: {model}")
