"""
tests.conftest
==============
"""
from configparser import ConfigParser
from pathlib import Path

import pytest

from gitspy import Git

from ._environ import GH_EMAIL, GH_NAME, REPO


@pytest.fixture(name="git")
def fixture_git() -> Git:
    """Get instantiated ``Git`` object.

    :return: Instantiated ``Git`` object.
    """
    return Git()


@pytest.fixture(name="mock_environment", autouse=True)
def fixture_mock_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, git: Git
) -> None:
    """Mock imports to reflect the temporary testing environment.

    :param tmp_path: Create and return temporary directory.
    :param monkeypatch: Mock patch environment and attributes.
    :param git: Instantiated ``Git`` object.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path / REPO))
    Path.cwd().mkdir()
    git.init(devnull=True)
    config = ConfigParser(default_section="")
    config.read_dict(
        dict(
            user={"name": GH_NAME, "email": GH_EMAIL},
            advice={"detachedHead": "false"},
            init={"defaultBranch": "master"},
        )
    )
    with open(Path.home() / ".gitconfig", "w", encoding="utf-8") as fout:
        config.write(fout)
