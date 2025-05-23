from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.document import Document
import logging
import os
from pathlib import Path
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
            cwd = os.getcwd()
            current_files = self.list_files_and_folders(cwd)
            for _file in current_files:
                yield Completion(_file, start_position=-len(current_word))
        # for path after @load
        if len(words) >= 2:
            if words[-2] == "@load":
                path = Path(current_word).expanduser()
                parent = path.parent
                prefix = path.name
                # ✅ Only continue if the path exists and is a directory
                if path.exists() and path.is_dir():
                    current_files = self.list_files_and_folders(str(path))
                    for _file in current_files:
                        yield Completion(_file, start_position=-len(current_word))
        yield from () #return  # <-- no completions yet

        # Your matching logic goes here

# from prompt_toolkit.completion import Completer, Completion, PathCompleter
# from prompt_toolkit.document import Document

# class SmartCompleter(Completer):
#     def __init__(self):
#         self.commands = ["@connect", "@load", "@exit"]
#         self.models = ["llama3", "gpt-4o", "mistral", "deepseek"]
#         self.path_completer = PathCompleter(expanduser=True)

#     def get_completions(self, document: Document, complete_event):

#         # text before cursor
#         text = document.text_before_cursor
#         # current word
#         current_word = document.get_word_before_cursor()
#         # words
#         words = text.strip().split()
#         print(document)
#         return []

#         # # Case 1: First word — suggest commands
        # if len(words) == 1 and not text.endswith(" "):
        #     for cmd in self.commands:
        #         if cmd.startswith(current_word):
        #             yield Completion(cmd, start_position=-len(current_word))

        # # Case 2: After "@connect" — suggest model names only if cursor is still on model
        # elif words and words[0] == "@connect":
        #     if not text.endswith(" "):  # Still typing the model
        #         for model in self.models:
        #             if model.startswith(current_word):
        #                 yield Completion(model, start_position=-len(current_word))

        # # Case 3: After "@load" — suggest paths only if cursor is on the file
        # elif words and words[0] == "@load":
        #     if not text.endswith(" "):  # Still typing file path
        #         fake_doc = Document(current_word, cursor_position=len(current_word))
        #         for comp in self.path_completer.get_completions(fake_doc, complete_event):
        #             yield comp
