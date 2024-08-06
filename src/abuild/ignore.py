from pathlib import Path
from abc import ABC, abstractmethod


class FileSkipperInterface(ABC):
    @abstractmethod
    def skip(self, path: Path) -> bool:
        pass

    @abstractmethod
    def update(self, ignorefile: Path) -> 'FileSkipperInterface':
        pass


class NeverSkip(FileSkipperInterface):
    def skip(self, path: Path) -> bool:
        return False

    @abstractmethod
    def update(self, ignorefile: Path) -> 'NeverSkip':
        return NeverSkip()

