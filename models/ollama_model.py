import requests
from typing import Generator
from .base import BaseModel
import json

class OllamaModel(BaseModel):

    def __init__(self, model_config: dict):
        self.model_name = model_config["name"]
        self.url = model_config["url"]
        self.temperature = float(model_config.get("temperature", 0.5))
        self.max_tokens = int(model_config.get("max_tokens", 2048))
        self.context = None  # ✅ Added to store context

    def stream(self, messages: list[dict]) -> Generator[str, None, None]:
        prompt = messages[-1]["content"]

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }

        if self.context:  # ✅ Include context only if available
            payload["context"] = self.context

        response = requests.post(f"{self.url}/api/generate", json=payload, stream=True)

        full_response = ""
        last_context = None  # ✅ Temp holder for final context

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode())
                    chunk = data.get("response", "")
                    full_response += chunk
                    yield chunk

                    if data.get("done") and "context" in data:  # ✅ Final context appears here
                        last_context = data["context"]
                except Exception as e:
                    print(f"[Ollama error parsing]: {e}")

        if last_context:  # ✅ Set context only once at end
            self.context = last_context

    def get_context(self):  # ✅ Optional helper
        return self.context

    def set_context(self, context):  # ✅ Optional helper
        self.context = context

