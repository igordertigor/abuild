import pytest
from pathlib import Path
from abuild import hashing
from abuild import ignore


def describe_all_files():
    @pytest.fixture
    def populated_dir(tmp_path: Path):
        (tmp_path / 'a_file.txt').write_text('a_file')
        (tmp_path / 'another_file.txt').write_text('another_file')
        (tmp_path / '.abuildignore').write_text('another_*')
        yield tmp_path

    def test_should_give_a_list_of_files(tmp_path: Path):
        assert sorted(hashing.all_files(tmp_path, hashing.NeverSkip())) == []

    def test_should_list_files_present(populated_dir: Path):
        assert list(
            map(
                str,
                sorted(hashing.all_files(populated_dir, hashing.NeverSkip())),
            )
        ) == [
            f'{str(populated_dir)}/.abuildignore',
            f'{str(populated_dir)}/a_file.txt',
            f'{str(populated_dir)}/another_file.txt',
        ]

    def test_should_drop_files_that_match_ignore(populated_dir: Path):
        assert list(
            map(
                str,
                sorted(hashing.all_files(populated_dir, ignore.GlobSkipper())),
            )
        ) == [
            f'{str(populated_dir)}/.abuildignore',
            f'{str(populated_dir)}/a_file.txt',
        ]
