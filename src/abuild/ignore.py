from typing import cast
from pathlib import Path
import fnmatch
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

    def update(self, ignorefile: Path) -> 'NeverSkip':
        return NeverSkip()


EmptyList = cast(list[str], object())


class GlobSkipper(FileSkipperInterface):
    patterns: list[str]

    def __init__(self, patterns: list[str] = EmptyList):
        if patterns is EmptyList:
            self.patterns = []
        else:
            self.patterns = patterns

    def skip(self, path: Path) -> bool:
        for pattern in self.patterns:
            if fnmatch.fnmatchcase(str(path), pattern):
                return True
            print(f'No match: {pattern} -- {str(path)}')
        return False

    def update(self, ignorefile: Path) -> 'GlobSkipper':
        new_patterns = [
            line.strip('\n') for line in ignorefile.read_text().splitlines()
        ]
        return GlobSkipper(self.patterns + new_patterns)

    def __repr__(self) -> str:
        return f'GlobSkipper({self.patterns})'

    def __str__(self) -> str:
        return repr(self)
