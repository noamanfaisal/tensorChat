from langchain_community.chat_models import ChatOpenAI
import os


class OpenAILangChainModel(ChatOpenAI):
    def __init__(self, model_config: dict):
        super().__init__(
            model_name=model_config["name"],
            temperature=float(model_config.get("temperature", 0.7)),
            streaming=True,
            api_key=model_config["api_key"]
        )
