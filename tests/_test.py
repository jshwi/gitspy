"""
tests._test
===========
"""
import os
from datetime import datetime
from pathlib import Path
from subprocess import CalledProcessError

import pytest

import gitspy

from ._environ import REAL_REPO, REPO


def test_pipe_to_file(git: gitspy.Git) -> None:
    """Test that the ``Subprocess`` class correctly writes to file.

    When the ``file`` keyword argument is used stdout should be piped to
    the filename provided.
    """
    path = Path.cwd() / "file.py"
    git.init(file=path)
    with open(path, encoding="utf-8") as fin:
        assert (
            fin.read().strip()
            == "Reinitialized existing Git repository in {}{}".format(
                Path.cwd() / ".git", os.sep
            )
        )


def test_arg_order_clone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, git: gitspy.Git
) -> None:
    """Test that the clone destination is always the last argument.

    :param tmp_path: Create and return a temporary directory for
        testing.
    :param monkeypatch: Mock patch environment and attributes.
    """
    called = []
    monkeypatch.setattr(
        "gitspy._subprocess.Subprocess.call",
        lambda x, *y, **_: called.extend(
            [f"{x} {' '.join(str(i) for i in y)}"]
        ),
    )
    path = tmp_path / REPO
    git.clone("--depth", "1", "--branch", "v1.1.0", REAL_REPO, path)
    assert [
        f"<Git (git)> clone --depth 1 --branch v1.1.0 {REAL_REPO} {path}"
    ] == called


def test_not_a_repository_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, git: gitspy.Git
) -> None:
    """Test error when Git command run in non-repository project.

    :param tmp_path: Create and return a temporary directory for
        testing.
    :param monkeypatch: Mock patch environment and attributes.
    """
    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))
    with pytest.raises(gitspy.exceptions.NotARepositoryError) as err:
        git.add(".")

    assert str(err.value) == "not a git repository"


def test_called_process_error_with_git(git: gitspy.Git) -> None:
    """Test regular Git command error."""
    with pytest.raises(CalledProcessError) as err:
        git.commit("-m", "Second initial commit")

    assert str(err.value) == (
        "Command 'git commit -m Second initial commit' returned non-zero exit "
        "status 1."
    )


def test_bare(capsys: pytest.CaptureFixture, git: gitspy.Git) -> None:
    """Test initialization of a bare repository.

    :param capsys: Capture system output.
    """
    remote = str(Path.home() / "origin.git")
    git.init("--bare", remote)
    git.remote("add", "origin", "origin")
    output = capsys.readouterr()
    assert f"Initialized empty Git repository in {remote}" in output.out


def test_command_not_found_error() -> None:
    """Test ``CommandNotFoundError`` warning with ``Subprocess``."""
    unique = datetime.now().strftime("%d%m%YT%H%M%S")
    # noinspection PyUnresolvedReferences
    proc = gitspy._subprocess.Subprocess(  # pylint: disable=protected-access
        unique
    )
    with pytest.raises(gitspy.exceptions.CommandNotFoundError) as err:
        proc.call()

    assert str(err.value) == f"{unique}: command not found..."


def test_key_in_context(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm there is no error raised when deleting temp key-value."""
    obj = {"key": "original-value"}
    monkeypatch.setattr("os.environ", obj)
    # noinspection PyUnresolvedReferences
    with gitspy._environ.TempEnvVar(  # pylint: disable=protected-access
        key="temp-value"
    ):
        assert obj["key"] == "temp-value"

    assert obj["key"] == "original-value"


def test_capture(git) -> None:
    """Test recording of sys output when called with ``capture``."""
    remote = str(Path.home() / "origin.git")
    git.init("--bare", remote, capture=True)
    output = git.stdout()
    assert len(output) == 1
    assert f"Initialized empty Git repository in {remote}/" in output
    assert not git.stdout()
