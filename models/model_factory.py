from models import ollama_langchain
from models.ollama_langchain import OllamaLangChainModel
from models.openai_langchain import OpenAILangChainModel

class ModelFactory:
    @staticmethod
    def create(model_config):
        model_type = model_config.get("model")

        if model_type == "openai":
            return OpenAILangChainModel(model_config)

        elif model_type == "ollama":
            return OllamaLangChainModel(model_config)

        else:
            raise ValueError(f"Unsupported model: {model_type}")
