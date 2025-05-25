import unittest
import time
import json
from pathlib import Path
from config import settings  # Import your settings module
from chat_state.factory import ChatStateFactory  # Import your ChatStateFactory
from models.model_factory import ModelFactory  # Optional, if you need to test with models
from config import settings  # Already imported, but repeated here for clarity

class TestOllamaChatState(unittest.TestCase):
    
    def setUp(self):
        # Use topic path from settings
        self.storage_path = settings.topics_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Create OllamaChatState via factory using model config
        model_name = settings.get_selected_model_name()
        model_config = settings.get_model(model_name)
        self.chat_state = ChatStateFactory.create(model_config, self.storage_path)
        
        # Reset topics for each test
        for file in self.storage_path.glob("*.json"):
            file.unlink()

    def test_new_topic_creation(self):
        self.chat_state.new_topic(model="gemma3-1b", initial_message="Hello!")
        self.assertIsNotNone(self.chat_state.current_topic)
        self.assertEqual(self.chat_state.get_model(), "gemma3-1b")
        self.assertEqual(self.chat_state.get_messages()[0]["content"], "Hello!")
        print("✅ New topic created with initial message.")

    def test_add_messages_with_numbering(self):
        self.chat_state.new_topic("gemma3-1b")
        self.chat_state.add_message("assistant", "Hi there!")
        self.chat_state.add_message("user", "How are you?")
        messages = self.chat_state.get_messages()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["number"], 1)
        self.assertEqual(messages[1]["number"], 2)
        print("✅ Messages added with correct numbering.")

    def test_save_and_load_topic(self):
        self.chat_state.new_topic("gemma3-1b")
        self.chat_state.add_message("assistant", "Hello there!")
        self.chat_state.save_current_topic()

        topic_id = self.chat_state.current_topic["id"]
        saved_file = self.storage_path / f"{topic_id}.json"
        self.assertTrue(saved_file.exists())

        with open(saved_file) as f:
            data = json.load(f)
            self.assertEqual(len(data["messages"]), 1)
            self.assertEqual(data["messages"][0]["content"], "Hello there!")
        print("✅ Topic saved to file with messages.")

    def test_context_set_and_get(self):
        context_data = [{"role": "system", "content": "Context info"}]
        self.chat_state.set_context(context_data)
        self.assertEqual(self.chat_state.get_context(), context_data)
        print("✅ Context set and retrieved.")

    def test_context_expiration(self):
        self.chat_state.set_context([{"role": "system", "content": "Context info"}])
        self.chat_state.context_ttl_seconds = 1  # Short TTL
        time.sleep(2)
        self.assertIsNone(self.chat_state.get_context())
        print("✅ Context expired as expected.")

if __name__ == "__main__":
    unittest.main()
