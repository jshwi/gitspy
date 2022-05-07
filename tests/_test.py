"""
tests._test
===========
"""
# pylint: disable=protected-access
import os
from pathlib import Path
from subprocess import CalledProcessError

import pytest

import gitspy

from . import REPO


def test_arg_order_clone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, git: gitspy.Git
) -> None:
    """Test that the clone destination is always the last argument.

    :param tmp_path: Create and return a temporary directory for
        testing.
    :param monkeypatch: Mock patch environment and attributes.
    :param git: Instantiated ``Git`` object.
    """
    real_repo = Path(__file__).parent.parent
    git.init(file=os.devnull)
    called = []
    monkeypatch.setattr(
        "gitspy._subprocess._Subprocess.call",
        lambda x, *y, **_: called.extend(
            [f"{x} {' '.join(str(i) for i in y)}"]
        ),
    )
    path = tmp_path / REPO
    git.clone("--depth", "1", "--branch", "v1.1.0", real_repo, path)
    assert [
        f"<Git (git)> clone --depth 1 --branch v1.1.0 {real_repo} {path}"
    ] == called


def test_not_a_repository_error(git: gitspy.Git) -> None:
    """Test error when Git command run in non-repository project.

    :param git: Instantiated ``Git`` object.
    """
    with pytest.raises(gitspy.exceptions.NotARepositoryError) as err:
        git.add(".")

    assert str(err.value) == "not a git repository"


def test_called_process_error_with_git(git: gitspy.Git) -> None:
    """Test regular Git command error.

    :param git: Instantiated ``Git`` object.
    """
    git.init(file=os.devnull)
    with pytest.raises(CalledProcessError) as err:
        git.commit("-m", "Second initial commit")

    assert str(err.value) == (
        "Command 'git commit -m Second initial commit' returned non-zero exit "
        "status 1."
    )


def test_bare(capsys: pytest.CaptureFixture, git: gitspy.Git) -> None:
    """Test initialization of a bare repository.

    :param capsys: Capture system output.
    :param git: Instantiated ``Git`` object.
    """
    remote = str(Path.home() / "origin.git")
    git.init(file=os.devnull)
    git.init("--bare", remote)
    git.remote("add", "origin", "origin")
    output = capsys.readouterr()
    assert f"Initialized empty Git repository in {remote}" in output.out


def test_key_in_context(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm there is no error raised when deleting temp key-value.

    :param monkeypatch: Mock patch environment and attributes.
    """
    key = "key"
    obj = {key: "original-value"}
    monkeypatch.setattr("os.environ", obj)
    # noinspection PyUnresolvedReferences
    with gitspy._environ.TempEnvVar(key="temp-value"):
        assert obj[key] == "temp-value"

    assert obj[key] == "original-value"
