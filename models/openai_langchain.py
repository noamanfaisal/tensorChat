from langchain_community.chat_models import ChatOpenAI

class OpenAILangChainModel(ChatOpenAI):
    def __init__(self, model_config: dict):
        super().__init__(
            model_name=model_config["name"],
            temperature=float(model_config.get("temperature", 0.7)),
            streaming=True
        )
