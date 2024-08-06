from typing import Iterable
import os
from pathlib import Path
from hashlib import md5

from .ignore import FileSkipperInterface, NeverSkip


def hash_directory(
    path: Path, skipper: FileSkipperInterface = NeverSkip()
) -> str:

    h = md5()
    for filepath in sorted(all_files(path, skipper)):
        h.update(filepath.read_bytes())
    return h.hexdigest()


def all_files(root: Path, skipper: FileSkipperInterface) -> Iterable[Path]:
    skippers: dict[str, FileSkipperInterface] = {}
    for dirname, _, filenames in os.walk(str(root)):
        ignore_file = Path(dirname) / '.abuildignore'
        if ignore_file.exists():
            parent_dir = str(Path(dirname).parent)
            skippers.setdefault(
                dirname,
                skippers.get(parent_dir, skipper).update(ignore_file),
            )
        else:
            parent_dir = str(Path(dirname).parent)
            skippers.setdefault(dirname, skippers.get(parent_dir, skipper))

        for filename in filenames:
            if not skippers[dirname].skip(Path(filename)):
                yield Path(os.path.join(dirname, filename))
