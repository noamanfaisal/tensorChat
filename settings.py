import configparser
from pathlib import Path

class Settings:
    def __init__(self, path="settings.ini"):
        self.path = Path(path).expanduser()
        self.config = configparser.ConfigParser()
        self.config.read(self.path)

    @property
    def topics_path(self):
        return Path(
            self.config.get("general", "topics_path"))

    @property
    def theme(self):
        return self.config.get("general", "theme", fallback="monokai")

    @property
    def chroma_db_path(self):
        return self.config.get("general", "chroma_db_path", fallback=str(Path.home() / ".chatui" / "chroma_db"))

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
        with self.path.open("w") as f:
            self.config.write(f)

    def is_file_too_large(self, path: str) -> bool:
        size_kb = Path(path).stat().st_size / 1024
        return size_kb > self.max_file_load_size_kb
