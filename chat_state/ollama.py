import json
import uuid
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from .base import BaseChatState
# import spacyi
# from keybert import KeyBERT
# from sentence_transformers import SentenceTransformer


class OllamaChatState(BaseChatState):

    def __init__(self, topics_path: Path, *args, **kwargs):
        self.base_path = topics_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.current_topic: Optional[Dict] = None
        self.context: Optional[list] = None
        self.context_last_updated: Optional[float] = None
        self.context_ttl_seconds: int = 1800  # 30 minutes
        self.output_number = 0
    
    @property
    def output(self):
        if self.current_topic:
            return self.current_topic['output_number']
        return 0
    
    def new_topic(self, model: str, initial_message: str = "") -> None:
        self._reset_context()
        topic_name = 'Untitled Topic'        
        self.current_topic = {
            "id": self._generate_topic_id(),
            "model": model,
            "created_at": datetime.utcnow().isoformat(),
            "messages": [],
            "output_number": 1,
            "name": topic_name,
        }
        if initial_message:
            self.add_message("user", initial_message)

    def reset(self, topic_id: str, model_name: str):
        self._reset_context()
        self.current_topic = {
            "id": topic_id,
            "model": model_name,
            "created_at": datetime.utcnow().isoformat(),
            "messages": [],
            "output_number": 1,
            "name": "Untitled Topic",
        }

    def add_message(self, role: str, content: str) -> None:
        if self.current_topic:
            if role == "user" and self.current_topic.get("name", "Untitled Topic") == "Untitled Topic":
                self.current_topic["name"] = self._generate_topic_name(content)
            if role == "assistant":
                self.output_number = self.current_topic.get("output_number", 1)
                self.current_topic["output_number"] = self.output_number + 1
                self.current_topic["messages"].append({
                    "role": role,
                    "content": content,
                    "output_number": self.output_number
                })
            else:
                self.current_topic["messages"].append({
                    "role": role,
                    "content": content
                })
            self.save_current_topic()

    def get_messages(self) -> List[Dict[str, str]]:
        return self.current_topic["messages"] if self.current_topic else []

    def get_model(self) -> str:
        return self.current_topic["model"] if self.current_topic else ""

    def save_current_topic(self) -> None:
        if self.current_topic:
            topic_id = self.current_topic["id"]
            filename = self.base_path / f"{topic_id}.json"
            with open(filename, "w") as f:
                json.dump(self.current_topic, f, indent=2)

    def _generate_topic_id(self) -> str:
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:6]

    def _reset_context(self):
        self.context = None
        self.context_last_updated = None

    def get_context(self) -> Optional[list]:
        if self.context and not self._is_context_expired():
            return self.context
        return None

    def set_context(self, context: list) -> None:
        self.context = context
        self.context_last_updated = time.time()

    def _is_context_expired(self) -> bool:
        if self.context_last_updated is None:
            return True
        return (time.time() - self.context_last_updated) > self.context_ttl_seconds
    
    def _generate_topic_name(self, text: str) -> str:
        if not text.strip():
            return "Untitled Topic"
        first_line = text.strip().split('\n')[0]
        return " ".join(first_line.strip().split()[:10])
    
    def load_topic(self, filename: str):
        with open(filename, "r") as f:
            self.current_topic = json.load(f)
        self._reset_context()  # Optional: reset context if desired
