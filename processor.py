from command_parser import CommandParser
from chat_state.factory import ChatStateFactory
from models.model_factory import ModelFactory
from config import settings
from prompt_processing.factory import PromptProcessorFactory  # ✅ NEW: your prompt processor factory

class MessageProcessor:

    def __init__(self):
        self.settings = settings
        self.parser = CommandParser()

        # Get model name and config
        model_name = self.settings.get_selected_model_name()
        model_config = self.settings.get_model(model_name)
        self.model = ModelFactory.create(model_config)

        # ✅ Load ChatState using key from settings.ini
        chat_state_key = self.settings.get_chat_state_name(model_name)
        self.chat_state = ChatStateFactory.load(chat_state_key, settings.topics_path)
        self.chat_state.new_topic(model=model_name)

        # ✅ Load PromptProcessor using key from settings.ini
        prompt_key = self.settings.get_prompt_processor_name(model_name)
        self.prompt_processor = PromptProcessorFactory.load(prompt_key)

    def process(self, message: str):
        parsed = self.parser.parse(message)

        if parsed["type"] == "prompt":
            return self._handle_prompt(parsed["raw"])
        elif parsed["type"] == "command":
            return self._handle_command(parsed)
        return "[System]: Unrecognized input."

    def _handle_prompt(self, text: str):
        last_context = self.chat_state.get_context()

        prompt = self.prompt_processor.prepare_prompt(
            context=last_context,
            history=self.chat_state.get_messages(),
            user_input=text
        )

        self.chat_state.add_message("user", text)

        full_response = ""
        for chunk in self.model.stream(prompt):
            full_response += chunk
            yield chunk

        self.chat_state.add_message("assistant", full_response)

        new_context = self.model.get_context()
        self.chat_state.set_context(new_context)

    def _handle_command(self, parsed: dict) -> str:
        cmd = parsed["command"]
        if cmd == "connect":
            model_name = parsed["args"]
            model_config = self.settings.get_model(model_name)
            self.model = ModelFactory.create(model_config)

            chat_state_key = self.settings.get_chat_state_name(model_name)
            self.chat_state = ChatStateFactory.load(chat_state_key, self.settings.topics_path)
            self.chat_state.new_topic(model=model_name)

            prompt_key = self.settings.get_prompt_processor_name(model_name)
            self.prompt_processor = PromptProcessorFactory.load(prompt_key)

            return f"[Connected to {model_name}]"

        return f"[Command '{cmd}' processed]"
