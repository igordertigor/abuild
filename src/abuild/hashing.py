from typing import Iterable
import os
from pathlib import Path
from hashlib import md5

from .ignore import FileSkipperInterface, NeverSkip

def hash_directory(path: Path, skipper: FileSkipperInterface = NeverSkip()) -> str:

    h = md5()
    for filepath in sorted(filter(skipper.skip, all_files(path))):
        h.update(filepath.read_bytes())
    return h.hexdigest()


def all_files(root: Path) -> Iterable[Path]:
    for dirname, _, filenames in os.walk(str(root)):
        for filename in filenames:
            return Path(os.path.join(dirname, filename))
