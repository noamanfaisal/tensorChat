from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.document import Document
import logging
import os
from pathlib import Path
from prompt_toolkit.document import Document
from prompt_toolkit.completion import PathCompleter
# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class SmartCompleter(Completer):
    def __init__(self):
        self.commands_in_start  = ["@connect", "@new_topic"]
        self.commands_anywhere = ["@load"]
        self.models = ["llama3", "gpt-4o", "mistral", "deepseek"]
        self.path_completer = PathCompleter(expanduser=True)
    
    def list_files_and_folders(self, path: str) -> list[str]:
        path_obj = Path(path).expanduser()
    
        # If user typed a partial path, like '~/Doc', expand to full directory
        if path_obj.is_file():
            path_obj = path_obj.parent

        if not path_obj.exists() or not path_obj.is_dir():
            return []

        entries = []
        for entry in sorted(path_obj.iterdir()):
            display_name = entry.name + ("/" if entry.is_dir() else "")
            entries.append(display_name)
    
        return entries

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        current_word = document.get_word_before_cursor()
        words = text.strip().split()
        # for commands in start
        if current_word == "@" and words[-1] == "@" and len(words) == 1:
            for cmd in (self.commands_in_start + self.commands_anywhere):
                if cmd.startswith(current_word):
                    yield Completion(cmd, start_position=-len(current_word))
        # for commands anywhere else
        if current_word == "@" and words[-1] == "@" and len(words) > 1:
            for cmd in self.commands_anywhere:
                if cmd.startswith(current_word):
                    yield Completion(cmd, start_position=-len(current_word))
        # for @connect
        if words[-1] == "@connect" and current_word == "" and len(words) == 1:
            for model in self.models:
                if model.startswith(current_word):
                    yield Completion(model, start_position=-len(current_word))
        # for @load
        if words[-1] == "@load" and current_word == "":
            completer = PathCompleter(expanduser=True)
            cwd = os.getcwd()
            doc = Document(cwd, cursor_position=len(cwd))
            completions = list(completer.get_completions(doc, complete_event=None))
            for c in completions:
                yield Completion(c.text, start_position=-len(current_word))

        # for path after @load
        if len(words) >= 2:
            if words[-2] == "@load":
                path_fragment = words[-1]
                completer = PathCompleter(expanduser=True)
                doc = Document(path_fragment, cursor_position=len(path_fragment))
                completions = list(completer.get_completions(doc, complete_event=None))
                for c in completions:
                    yield Completion(c.text, start_position=-len(current_word))

