from abc import ABC, abstractmethod
from typing import Generator

class BaseModel(ABC):
    @abstractmethod
    def stream(self, messages: list[dict]) -> Generator[str, None, None]:
        """Stream response as chunks"""
        pass
    @abstractmethod
    def get_context(self):  # ✅ Optional helper
        pass
    @abstractmethod
    def set_context(self, context):  # ✅ Optional helper
        pass
