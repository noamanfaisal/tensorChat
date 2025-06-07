from os import XATTR_SIZE_MAX
from langchain.memory import ConversationBufferMemory
from tinydb import TinyDB, where
from datetime import datetime
import json
from typing import List, Dict
from pydantic import Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import trim_messages
from datetime import datetime
import uuid

class ConversationThread(ConversationBufferMemory):

    session_id: str = Field(default=None)
    db: TinyDB = Field(default=None)
    topics_table: TinyDB.table_class = Field(default=None)  # or just `Any
    current_topic: dict = Field(default_factory=dict)
    # TOPIC_TABLE_NAME = "topics"
    
    def __init__(self, session_id=None, db_path='chat_memory.json', **kwargs):
        
        super().__init__(**kwargs)
        if session_id == None:
            self.session_id = self._generate_new_topic_id()
        else:
            self.session_id = session_id
        self.db = TinyDB(db_path)
        self.topics_table = self.db.table("topics")

    def save_context(self, inputs, outputs):
        # First, let LangChain handle the memory
        super().save_context(inputs, outputs)
        # Prepare and persist this interaction to TinyDB
        data = {
            "session_id": self.session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "input": json.dumps(inputs),   # JSON serialization ensures compatibility
            "output": json.dumps(outputs)
        }
        self.topics_table.insert(data)
        
    def get_trimmed_messages(self, model, max_tokens=2048, buffer_tokens=200, strategy="last") -> List[dict]:
        """
        Return the chat memory trimmed to fit within max_tokens - buffer_tokens.
        """
        full_history = self.get_messages()

        trimmer = trim_messages(
            max_tokens=max_tokens - buffer_tokens,
            strategy=strategy,
            token_counter=model,  # Must have a get_num_tokens method
            include_system=True,
            allow_partial=False,
            start_on="human"
        )

        return trimmer.invoke(full_history)
    
    def start_new_topic(self, model: str = "unknown", name: str = "Untitled Topic") -> str:
        
        self.clear()
        topic_id = self._generate_new_topic_id()
        self.session_id = topic_id

        self.topics_table.insert({
            "id": topic_id,
            "model": model,
            "created_at": datetime.utcnow().isoformat(),
            "name": name
        })

        return topic_id
    
    def get_messages(self) -> List[Dict[str, str]]:
        return self.chat_memory.messages if hasattr(self.chat_memory, 
                                                    "messages") else []

    def load_topic(self, filename: str):
        """
        Load a topic from a file and populate the ConversationBufferMemory buffer.
        """
        with open(filename, "r") as f:
            loaded_data = json.load(f)

        # Reset context before loading
        self._reset_context()

        # Populate buffer with loaded messages
        messages = loaded_data.get("messages", [])
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            self.add_message(role, content)

        # Optionally set current_topic to reflect loaded topic metadata
        self.current_topic = loaded_data

    def add_message(self, role: str, content: str):
        if role == "user":
            breakpoint()
            message = HumanMessage(content=content)
            # If current topic is still 'Untitled Topic', update name
            if self.topics_table.contains(where('id') == self.session_id):
                current = self.topics_table.get(where('id') == self.session_id)
                if current.get("name") == "Untitled Topic":
                    self.topics_table.update({"name": content[:240]}, where('id') == self.session_id)

        elif role == "assistant":
            message = AIMessage(content=content)
        elif role == "system":
            message = SystemMessage(content=content)
        else:
            raise ValueError(f"Unsupported role: {role}")
    
        self.chat_memory.add_message(message)
    
    def _generate_new_topic_id(self):
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:6]
    
    def list_all_topics(self) -> List[Dict[str, str]]:
        return sorted(
            self.db.table("topics").all(),
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )
