
import json
from pathlib import Path
import uuid
from datetime import datetime
from typing import List, Dict
from .base import BaseChatState

class OllamaChatState(BaseChatState):
    def __init__(self, topics_path: Path):
        self.base_path = topics_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.current_topic = None

    def new_topic(self, model: str, initial_message: str = "") -> None:
        self.save_current_topic()
        self.current_topic = {
            "id": self._generate_topic_id(),
            "model": model,
            "created_at": datetime.utcnow().isoformat(),
            "messages": [],
        }
        if initial_message:
            self.add_message("user", initial_message)

    def add_message(self, role: str, content: str) -> None:
        if self.current_topic:
            self.current_topic["messages"].append({
                "role": role,
                "content": content
            })
            self._save_topic_atomic()

    def get_messages(self) -> List[Dict[str, str]]:
        return self.current_topic["messages"]

    def get_model(self) -> str:
        return self.current_topic["model"]

    def save_current_topic(self) -> None:
        if self.current_topic and self.current_topic["messages"]:
            filename = self.base_path / f"{self.current_topic['id']}.json"
            with open(filename, "w") as f:
                json.dump(self.current_topic, f, indent=2)
            print(f"Topic saved to {filename}")

    def _save_topic_atomic(self):
        filename = self.base_path / f"{self.current_topic['id']}.json"
        tmp_filename = filename.with_suffix(".json.tmp")
        with open(tmp_filename, "w") as f:
            json.dump(self.current_topic, f, indent=2)
        tmp_filename.rename(filename)

    def _generate_topic_id(self) -> str:
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:6]


