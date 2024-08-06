from pathlib import Path
from abuild.ignore import GlobSkipper


def describe_glob_skipper():
    def test_should_skip_based_on_glob():
        assert GlobSkipper(['test*']).skip(Path('testfile'))
