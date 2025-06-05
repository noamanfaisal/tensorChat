from langchain_community.chat_models import ChatOllama  
# ✅ Comes from LangChain community package

class OllamaLangChainModel(ChatOllama):
    def __init__(self, model_config: dict):
        super().__init__(
            model=model_config["name"],
            temperature=float(model_config.get("temperature", 0.7)),
            base_url=model_config.get("url")  # ✅ Add this
        )
