import requests
from .base_model import basemodel

class ollamamodel(basemodel):
    def __init__(self, config: dict):
        self.url = config["url"]
        self.temperature = float(config.get("temperature", 0.5))
        self.model = config["name"]

    def stream(self, messages):
        prompt = messages[-1]["content"]
        response = requests.post(f"{self.url}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": true,
            "options": {"temperature": self.temperature},
        }, stream=true)

        for line in response.iter_lines():
            if line:
                yield line.decode()

