from models import ollama_langchain
from models.ollama_langchain import OllamaLangChainModel
from models.openai_langchain import OpenAILangChainModel

class ModelFactory:
    @staticmethod
    def create(model_config):
        load_model_class = model_config.get("load_model_class")
 
        if load_model_class == "openai":
            return OpenAILangChainModel(model_config)

        elif load_model_class == "ollama":
            return OllamaLangChainModel(model_config)

        else:
            raise ValueError(f"Unsupported model: {model_type}")
