"""
gitspy._subprocess
==================
"""
import os as _os
import subprocess as _sp
import typing as _t
from pathlib import Path as _Path

from spall import Subprocess as _Subprocess

from ._environ import TempEnvVar as _TempEnvVar


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
        with _TempEnvVar(
            GIT_WORK_TREE=str(gitdir.parent), GIT_DIR=str(gitdir)
        ):
            if "--bare" in args:
                del _os.environ["GIT_WORK_TREE"]

            return super().call(*args, **kwargs)
