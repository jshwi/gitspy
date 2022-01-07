"""
gitspy._subprocess
==================
"""
import os as _os
import subprocess as _sp
import typing as _t
from pathlib import Path as _Path

from spall import Subprocess as _Subprocess

from . import exceptions as _exceptions
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
        super().__init__("git", positionals=self.commands, loglevel="debug")

    def call(self, *args: str, **kwargs: _t.Union[bool, str]) -> int:
        """Call partial git command instantiated in superclass.

        :param args: Command's positional arguments.
        :key file: File path to write the stdout stream to.
        :key capture: Pipe stream to self.
        :key devnull: Suppress output.
        :key suppress: Suppress errors and continue running.
        :raises NotARepositoryError: If not run from within a
            repository.
        :raises CalledProcessError: If error occurs in subprocess.
        :return: Exit status.
        """
        git_dir = _Path.cwd() / ".git"
        with _TempEnvVar(GIT_WORK_TREE=str(_Path.cwd()), GIT_DIR=str(git_dir)):
            if "--bare" in args:
                del _os.environ["GIT_WORK_TREE"]

            try:
                return super().call(*args, **kwargs)

            except _sp.CalledProcessError as err:
                if not git_dir.is_dir():
                    raise _exceptions.NotARepositoryError from err

                raise err
