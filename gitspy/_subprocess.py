"""
gitspy._subprocess
==================
"""
import contextlib as _contextlib
import os as _os
import subprocess as _sp
import typing as _t
from pathlib import Path as _Path

from spall import Subprocess as _Subprocess


class Git(_Subprocess):
    """Git commands as class attributes.

    @DynamicAttrs
    """

    def __init__(self) -> None:
        self.commands = [
            i.lstrip().split()[0]
            for i in _sp.check_output(["git", "help", "--all"])
            .decode()
            .splitlines()
            if i.startswith("   ")
        ]
        super().__init__("git", positionals=self.commands)

    def _get_gitdir(self, path: _Path) -> _t.Optional[_Path]:
        # find and return the path to the repository's .git directory
        # start with provided path and any parent up to / where None is
        # returned if working outside a repository
        gitdir = path / ".git"
        if gitdir.is_dir():
            return gitdir

        if path == _Path("/"):
            return None

        return self._get_gitdir(path.parent)

    def call(self, *args: str, **kwargs: _t.Union[bool, str]) -> int:
        """Call partial git command instantiated in superclass.

        :param args: Command's positional arguments.
        :key file: File path to write the stdout stream to.
        :key capture: Pipe stream to self.
        :key devnull: Suppress output.
        :key suppress: Suppress errors and continue running.
        :raises CalledProcessError: If error occurs in subprocess.
        :return: Exit status.
        """
        cwd = _Path.cwd().absolute()
        gitdir = self._get_gitdir(cwd) or cwd / ".git"
        try:
            _os.environ.update(
                GIT_DIR=str(gitdir), GIT_WORK_TREE=str(gitdir.parent)
            )

            # silence stderr to avoid duplicates if error raised again
            # and to avoid writing to stderr if second command succeeds
            with _contextlib.redirect_stderr(None):
                return super().call(*args, **kwargs)

        # options such as `--bare` won't allow `GIT_WORK_TREE` to be set
        except _sp.CalledProcessError:
            del _os.environ["GIT_WORK_TREE"]
            return super().call(*args, **kwargs)
