"""
tests.conftest
==============
"""
from configparser import ConfigParser
from pathlib import Path

import pytest

from gitspy import Git

from . import REPO


@pytest.fixture(name="mock_environment", autouse=True)
def fixture_mock_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Mock imports to reflect the temporary testing environment.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path / REPO))
    Path.cwd().mkdir()


@pytest.fixture(name="setup_git", autouse=True)
def fixture_setup_git() -> None:
    """Setup ~/.gitconfig in mocked "$HOME" directory."""
    config = ConfigParser(default_section="")
    config.read_dict(
        dict(
            user={"name": "test_name", "email": "test_name@test_email.com"},
            advice={"detachedHead": "false"},
            init={"defaultBranch": "master"},
        )
    )
    with open(Path.home() / ".gitconfig", "w", encoding="utf-8") as fout:
        config.write(fout)


@pytest.fixture(name="git")
def fixture_git() -> Git:
    """Get instantiated ``Git`` object.

    :return: Instantiated ``Git`` object.
    """
    return Git()
