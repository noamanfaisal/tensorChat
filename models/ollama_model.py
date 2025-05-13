import requests
from typing import Generator
from .base import BaseModel
from config import settings
import json

class OllamaModel(BaseModel):

    def __init__(self, model_config: dict):
        self.model_name = model_config["name"]
        self.url = model_config["url"]
        self.temperature = float(model_config.get("temperature", 0.5))
        self.max_tokens = int(model_config.get("max_tokens", 2048))
        
    def stream(self, messages: list[dict]) -> Generator[str, None, None]:
        prompt = messages[-1]["content"]
        response = requests.post(f"{self.url}/api/generate", json={
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            },
        }, stream=True)

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode())
                    yield data.get("response", "")
                except Exception as e:
                    print(f"[Ollama error parsing]: {e}")
