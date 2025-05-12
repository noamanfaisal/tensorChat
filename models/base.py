from abc import ABC, abstractmethod
from typing import Generator

class BaseModel(ABC):
    @abstractmethod
    def stream(self, messages: list[dict]) -> Generator[str, None, None]:
        """Stream response as chunks"""
        pass

