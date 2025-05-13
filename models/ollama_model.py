import requests
from typing import Generator
from base import BaseModel
from config import settings
import json

class OllamaModel(BaseModel):

    def __init__(self, model_name: str = "model_gemma3-1b"):
        import pdb;pdb.set_trace()
        config = settings.get_model(model_name)

        self.model_name = model_name
        self.model = config["name"]
        self.url = config["url"]
        self.temperature = float(config.get("temperature", 0.5))
        self.max_tokens = int(config.get("max_tokens", 2048))

    def stream(self, messages: list[dict]) -> Generator[str, None, None]:
        prompt = messages[-1]["content"]
        response = requests.post(f"{self.url}/api/generate", json={
            "model": self.model,
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
