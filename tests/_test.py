"""
tests._test
===========
"""
from pathlib import Path
from subprocess import CalledProcessError

import pytest

import gitspy

from ._environ import REAL_REPO, REPO


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
        "gitspy._subprocess._Subprocess.call",
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
