from .command_parser import CommandParser
from .chat_state import ChatState  # if needed

class MessageProcessor:
    def __init__(self):
        self.parser = CommandParser()
        self.chat_state = ChatState()  # to track model, topic, etc.

    async def process(self, message: str) -> str:
        parsed = self.parser.parse(message)

        if parsed["type"] == "prompt":
            return await self._handle_prompt(parsed["raw"])

        elif parsed["type"] == "command":
            return self._handle_command(parsed)

        return "[System]: Unrecognized input."

    async def _handle_prompt(self, text: str) -> str:
        # add message to state
        self.chat_state.add_message("user", text)

        model_name = self.chat_state.get_model()
        model_response = await self._send_to_model(model_name, self.chat_state.get_messages())

        self.chat_state.add_message("assistant", model_response)
        return model_response

    def _handle_command(self, parsed: dict) -> str:
        cmd = parsed["command"]
        if cmd == "connect":
            model_name = parsed["args"]
            self.chat_state.new_topic(model=model_name)
            return f"[Connected to {model_name}]"
        return f"[Command '{cmd}' processed]"

    async def _send_to_model(self, model_name: str, messages: list[str]) -> str:
        # TODO: call OpenAI/Ollama here
        return f"[Fake model reply to '{messages[-1]['content']}']"
