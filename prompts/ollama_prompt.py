from .base import PromptProcessor

class OllamaPromptProcessor(PromptProcessor):
    def prepare_prompt(self, context, history, user_input, system=None) -> list[dict]:
        messages = []

        if system:
            messages.append({"role": "system", "content": system})

        if context:
            # Optional: Include context as metadata message
            messages.append({"role": "context", "content": str(context)})

        messages.extend(history)  # history is already in {"role": ..., "content": ...} format

        messages.append({"role": "user", "content": user_input})

        return messages

