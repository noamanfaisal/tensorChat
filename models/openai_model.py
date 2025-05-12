import openai
from .base_model import BaseModel

class OpenAIModel(BaseModel):
    def __init__(self, config: dict):
        self.api_key = config["api_key"]
        self.temperature = float(config.get("temperature", 0.7))
        self.max_tokens = int(config.get("max_tokens", 1024))
        openai.api_key = self.api_key

    def stream(self, messages):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True
        )
        for chunk in response:
            delta = chunk['choices'][0]['delta']
            yield delta.get("content", "")

