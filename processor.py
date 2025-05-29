from command_parser import CommandParser
from chat_state.factory import ChatStateFactory
from models.model_factory import ModelFactory
from config import settings
from prompts.factory import PromptProcessorFactory  # ✅ NEW: your prompt processor factory
from prompts.action_processor import PromptActionHandler
class MessageProcessor:

    def __init__(self):
        self.settings = settings
        self.parser = CommandParser()
        # Get model name and config
        model_name = self.settings.get_selected_model_name()
        # loading model config
        model_config = self.settings.get_model(model_name)
        # breakpoint()
        # loading model
        self.model = ModelFactory.create(model_config)
        # ✅ Load ChatState using key from settings.ini
        self.chat_state = ChatStateFactory.create(model_config, settings.topics_path)
        # new topic for chat_state
        self.chat_state.new_topic(model=model_name)
        # ✅ Load PromptProcessor using key from settings.ini
        self.prompt_processor = PromptProcessorFactory.create(model_config)
        self.action_processor = PromptActionHandler()

    def process(self, message: str):
        parsed = self.parser.parse(message)

        if parsed["type"] == "prompt":
            return self._handle_prompt(parsed)
        elif parsed["type"] == "command":
            return self._handle_command(parsed)
        return "[System]: Unrecognized input."
    
    def _handle_prompt(self, parsed: dict):
        # breakpoint()
        text = parsed['raw']  # Already parsed, so use 'raw' text
        last_context = self.chat_state.get_context()
        # Use parsed data directly from 'prompt'
        action_result = self.action_processor.process(parsed)
        # get loaded files if there are any
        loaded_files = action_result.get("loaded_files", [])
        #  Get model name and output number
        model_name = self.chat_state.get_model()
        output_number = self.chat_state.output

        # Format the header with Markdown and color (e.g., using ANSI or Markdown)
        header = f"\n```ansi\n[Model: {model_name} | Output #{output_number}\n```\n"

        # Yield the header first
        yield header
        final_prompt = self.prompt_processor.prepare_prompt(
            context=last_context,
            history=None,
            user_input=text,
            system=None,
            loaded_files=loaded_files
        )

        self.chat_state.add_message("user", text)

        full_response = ""
        for chunk in self.model.stream(final_prompt):
            full_response += chunk
            yield chunk

        self.chat_state.add_message("assistant", full_response)
        new_context = self.model.get_context()
        self.chat_state.set_context(new_context)
    
    def _initialize_model(self, model_name):
        self.settings.set_selected_model(model_name)
        model_config = self.settings.get_model(model_name)
        self.model = ModelFactory.create(model_config)
        self.chat_state = ChatStateFactory.create(model_config, settings.topics_path)
        self.chat_state.new_topic(model=model_name)
        self.prompt_processor = PromptProcessorFactory.create(model_config)
        self.action_processor = PromptActionHandler()

    def _handle_command(self, parsed: dict) -> str:
        cmd = parsed["command"]
        if cmd == "new_topic":
            model_name = self.settings.get_selected_model_name()
            self._initialize_model(model_name)
            return "[CLEAR_SCREEN]"

        if cmd == "connect":
            model_name = parsed["args"]
            self._initialize_model(model_name)
            return f"[Connected to {model_name} and new topic initialized]"

        return f"[Command '{cmd}' processed]"
