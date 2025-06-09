from command_parser import CommandParser
from config import settings
from session_manager import SessionManager
from conversation_thread import ConversationThread
from models.model_factory import ModelFactory
import prompt_template
import uuid
from typing import AsyncGenerator
from copy import deepcopy

class MessageProcessor:
    def __init__(self):
        self.settings = settings
        self.parser = CommandParser()
        self.session = SessionManager()

        # Get model configuration and create model via factory
        model_config_name = self.settings.get_selected_model_name()
        self.model_config = self.settings.get_model(model_config_name)
        # initiate model
        self.model = ModelFactory.create(self.model_config)
        # Initialize persistent memory
        # self.session.set('current_topic_id', topic_id)
        self.memory = ConversationThread(deepcopy(dict(self.model_config)))
        # Load dynamic prompt processor
        self.prompt_processor = prompt_template.Factory.create()

    def process(self, message: str) -> AsyncGenerator[str, None]:
        parsed = self.parser.parse(message)

        if parsed["type"] == "prompt":
            return self._handle_prompt(parsed)
        elif parsed["type"] == "command":
            return self._handle_command(parsed)
        return "[System]: Unrecognized input."
    

    def _handle_prompt(self, parsed: dict) -> AsyncGenerator[str, None]:
        text = parsed['raw']
        filepaths = parsed.get("filepaths", [])
        output_number = len(self.memory.get_messages()) // 2 + 1
        model_name = self.model_config["model"]
    
        yield f"\n```ansi\n[Model: {model_name} | Output #{output_number}]\n```\n"

        # Inject file contents into user input
        resolved_input = inject_files_into_text(text, filepaths, base_path=settings.data_path) if filepaths else text

        # Get trimmed context from memory
        trimmed_history = self.memory.get_trimmed_messages(
            model=self.model,
            max_tokens=int(self.model_config.get("max_tokens", 4096)),
            buffer_tokens=512
        )
        
        # Format final prompt with trimmed history + user input
        template = prompt_template.Factory.create("default")
        final_messages = template.format_messages(
            history=trimmed_history,
            input=resolved_input
        )
        # Store the user message
        self.memory.add_message("user", text)
        # Stream model output
        full_response = ""
        for chunk in self.model.stream(final_messages):
            text_chunk = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_response += text_chunk
            yield text_chunk

        # Save assistant message and full context
        self.memory.add_message("assistant", full_response)
        self.memory.save_context({"input": text}, {"response": full_response})
        

    def _handle_command(self, parsed: dict) -> AsyncGenerator[str, None]:
        cmd = parsed["command"]

        if cmd == "list_topics":
            # topics = self.memory.list_all_topics()
            # yield topics
            topics = self.memory.list_all_topics()

            if not topics:
                yield "### No topics found."

            yield "### 📚 Available Topics\n"
            for i, t in enumerate(topics, 1):
                    name = t.get("name", "Untitled")
                    model = t.get("model", "unknown")
                    created = t.get("created_at", "")
                    topic_id = t.get("id", "")

                    yield f"{i}. **{name}** — `{model}` @ `{created}`    - ID: `{topic_id}`\n"
        
        if cmd == "new_topic":
            new_topic_id = \
                self.memory.start_new_topic(model=self.model_config["model"])
            yield f"[New topic {new_topic_id} initialized]"

        if cmd == "connect":
            model_name = parsed["args"]
            if model_name in self.settings.get_all_model_names():
                self.settings.set_selected_model(model_name)
                # Get model configuration and create model via factory
                model_config_name = self.settings.get_selected_model_name()
                self.model_config = self.settings.get_model(model_config_name)
                self.model = ModelFactory.create(self.model_config)
                yield f"\n```ansi\n\u001b✔ Connected to {model_name}\u001b```\n"
                # yield f"✅ **Connected to `{model_name}`**"
                # yield f"[Connected to {model_name}]"
            else:
                yield f"{model_name} model name must be in model list that {self.settings.get_all_model_names()}"
                

    def _generate_new_topic_id(self):
        return datetime.utcnow().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:6]
