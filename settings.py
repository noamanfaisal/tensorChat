import configparser
from pathlib import Path
import os

class Settings:
    
    def __init__(self, path="settings.ini"):
        self.path = Path(path)
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.data_path = '~/'


    @property
    def submit_key(self):
        return self.config.get("general", "submit_key")

    @property
    def topics_path(self):
        return Path(self.config.get("general", "topics_path"))

    @property
    def theme(self):
        return self.config.get("general", "theme", fallback="monokai")

    @property
    def chroma_db_path(self):
        return self.config.get("general", "chroma_db_path", 
                        fallback=str(Path.home() / ".chatui" / "chroma_db"))

    @property
    def max_file_load_size_kb(self):
        return self.config.getint("general", "max_file_load_size_kb", fallback=200)

    def get_selected_model_name(self):
        return self.config.get("general", "selected_model", fallback=None)

    def get_model(self, name=None):
        name = name or self.get_selected_model_name()
        section = f"model_{name}"
        if not self.config.has_section(section):
            raise ValueError(f"Model '{name}' not found.")
        self.resolve_url_and_api_key(section)
        return dict(self.config.items(section))

    def get_all_models(self):
        prefix = "model_"
        models = []
        for section in self.config.sections():
            if section.startswith(prefix):
                name = section[len(prefix):]
                model_data = dict(self.config.items(section))
                model_data["name"] = name
                models.append(model_data)
        return models

    def set_selected_model(self, name: str):
        section = f"model_{name}"
        if not self.config.has_section(section):
            raise ValueError(f"Model '{name}' does not exist.")
        self.config.set("general", "selected_model", name)
        # with self.path.open("w") as f:
        #     self.config.write(f)
    
    def resolve_url_and_api_key(self, section: str):

        has_url      = self.config.has_option(section, "url")
        has_api_key = self.config.has_option(section, "api_key")

        if not (has_url or has_api_key):
            raise ValueError(f"Model must define at least one of 'url' or 'api_key' in section [{section}].")

        if has_url and has_api_key:
            raise ValueError(f"Model must define only one of 'url' or 'api_key' in section [{section}].")

        if has_api_key:
            key = self.config[section]["api_key"]
            if key is None or key == "":
                raise ValueError(f"Model cannot have an empty 'api_key' field in section [{section}].")
            self.config[section]["api_key"] = os.getenv(key[1:]) if key.startswith("$") else key
            

    def is_file_too_large(self, path: str) -> bool:
        size_kb = Path(path).stat().st_size / 1024
        return size_kb > self.max_file_load_size_kb

    # ✅ New helper methods for factory lookup
    def get_chat_state_name(self, model_name=None) -> str:
        return self.get_model(model_name).get("chat_state", "base")

    def get_prompt_processor_name(self, model_name=None) -> str:
        return self.get_model(model_name).get("prompt_processor", "default")

    def get_all_model_names(self) -> list[str]:
        return [section[len("model_"):] for section in self.config.sections() if section.startswith("model_")]

# import configparser
# from pathlib import Path

# class Settings:
    
#     def __init__(self, path="settings.ini"):
#         self.path = Path(path)
#         self.config = configparser.ConfigParser()
#         self.config.read(self.path)

#     @property
#     def topics_path(self):
#         return Path(
#             self.config.get("general", "topics_path"))

#     @property
#     def theme(self):
#         return self.config.get("general", "theme", fallback="monokai")

#     @property
#     def chroma_db_path(self):
#         return self.config.get("general", "chroma_db_path", fallback=str(Path.home() / ".chatui" / "chroma_db"))

#     @property
#     def max_file_load_size_kb(self):
#         return self.config.getint("general", "max_file_load_size_kb", fallback=200)

#     def get_selected_model_name(self):
#         return self.config.get("general", "selected_model", fallback=None)

#     def get_model(self, name=None):
#         name = name or self.get_selected_model_name()
#         section = f"model_{name}"
#         if not self.config.has_section(section):
#             raise ValueError(f"Model '{name}' not found.")
#         return dict(self.config.items(section))

#     def get_all_models(self):
#         prefix = "model_"
#         models = []
#         for section in self.config.sections():
#             if section.startswith(prefix):
#                 name = section[len(prefix):]
#                 model_data = dict(self.config.items(section))
#                 model_data["name"] = name
#                 models.append(model_data)
#         return models

#     def set_selected_model(self, name: str):
#         section = f"model_{name}"
#         if not self.config.has_section(section):
#             raise ValueError(f"Model '{name}' does not exist.")
#         self.config.set("general", "selected_model", name)
#         with self.path.open("w") as f:
#             self.config.write(f)

#     def is_file_too_large(self, path: str) -> bool:
#         size_kb = Path(path).stat().st_size / 1024
#         return size_kb > self.max_file_load_size_kb
