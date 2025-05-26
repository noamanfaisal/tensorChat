from .base import PromptProcessor
import re
from typing import List, Dict

class OllamaPromptProcessor(PromptProcessor):
    def prepare_prompt(self, context, history, user_input, system=None, loaded_files=None) -> list[dict]:
        messages = []

        # Step 1: Handle system message
        if system:
            messages.append({"role": "system", "content": system})

        # Step 2: Handle context (as metadata or additional message)
        if context:
            # Optional: join context if it's a list
            if isinstance(context, list):
                context_content = " ".join(str(c) for c in context)
            else:
                context_content = str(context)
            messages.append({"role": "context", "content": context_content})

        # Step 3: Extend with history if available
        if history:
            messages.extend(history)

        # Step 4: Handle loaded files (if applicable)
        if loaded_files:
            # Replace @load references in user_input
            user_input = self.replace_loads_in_text(user_input, loaded_files.copy())

        # Step 5: Add the final user input
        messages.append({"role": "user", "content": user_input})

        return messages
    
    def replace_loads_in_text(self, text: str, loaded_files: List[Dict[str, str]]) -> str:
        load_pattern = re.compile(r'@load\s+([^\s#]+)')

        def replacer(match):
            if loaded_files:
                file_info = loaded_files.pop(0)
                return file_info["content"]
            return "[Missing content]"

        return load_pattern.sub(replacer, text)
