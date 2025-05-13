from command_parser import CommandParser
from chat_state import ChatState
from models.model_factory import ModelFactory
from config import settings

class MessageProcessor:

    def __init__(self):
        self.settings = settings
        self.parser = CommandParser()
        self.chat_state = ChatState(settings.topics_path)
        # get model name
        model_name = self.settings.get_selected_model_name()
        
        self.chat_state.new_topic(model=model_name)
        model_config = self.settings.get_model(model_name)
        self.model = ModelFactory.create(model_config)
    
    async def process(self, message: str) -> str:
        parsed = self.parser.parse(message)
        if parsed["type"] == "prompt":
            return await self._handle_prompt(parsed["raw"])
        elif parsed["type"] == "command":
            return self._handle_command(parsed)
        return "[System]: Unrecognized input."
    
    def _handle_prompt(self, text: str):
        self.chat_state.add_message("user", text)

        full_response = ""
        for chunk in self.model.stream(self.chat_state.get_messages()):
            full_response += chunk
            yield chunk  # ✅ yield as it comes

        self.chat_state.add_message("assistant", full_response)
    # async def _handle_prompt(self, text: str) -> str:
    #     self.chat_state.add_message("user", text)
    #     # Just pass messages to the interface-compliant model
    #     full_response = ""
    #     for chunk in self.model.stream(self.chat_state.get_messages()):
    #         full_response += chunk
    #     self.chat_state.add_message("assistant", full_response)
    #     return full_response

    def _handle_command(self, parsed: dict) -> str:
        cmd = parsed["command"]
        if cmd == "connect":
            model_name = parsed["args"]
            self.chat_state.new_topic(model=model_name)
            model_config = self.settings.get_model(model_name)
            self.model = ModelFactory.create(model_config)
            return f"[Connected to {model_name}]"
        return f"[Command '{cmd}' processed]"
