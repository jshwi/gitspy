"""
gitspy._subprocess
==================
"""
import functools as _functools
import logging as _logging
import os as _os
import shutil as _shutil
import subprocess as _sp
import sys as _sys
import typing as _t
from pathlib import Path as _Path

from . import exceptions as _exceptions
from ._environ import TempEnvVar as _TempEnvVar


class Subprocess:
    """Object-oriented Subprocess.

    ``exe`` is a mandatory argument used to construct the subprocess
    executable.

    Default ``file``, ``suppress``, ``capture``, and ``devnull`` values
    can be set when instantiating the object to be overridden later when
    using ``call``, or simply set through the ``call`` method alone.

    :param cmd: Subprocess executable.
    :key loglevel: Loglevel for non-error logging.
    :param positionals: List of positional arguments to set as attributes
        if not None.
    :key file: File path to write stream to if not None.
    :key capture: Collect output array.
    :key log: Pipe stdout to logging instead of console.
    :key devnull: Send output to /dev/null.
    :raise CommandNotFoundError: Raise if instantiated subprocess cannot
        exist.
    """

    def __init__(
        self,
        cmd: str,
        loglevel: str = "error",
        positionals: _t.Optional[_t.Iterable[str]] = None,
        **kwargs: _t.Union[bool, str],
    ) -> None:
        self._cmd = cmd
        self._loglevel = loglevel
        self._kwargs = kwargs
        self._stdout: _t.List[str] = []
        self._logger = _logging.getLogger(cmd)
        if positionals is not None:
            self._set_positionals(positionals)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ({self._cmd})>"

    def __setattr__(self, key: str, value: _t.Any) -> None:
        # pylint: disable=useless-super-delegation
        # not useless; silences `mypy` with `_t.Any` and dynamic attrs
        super().__setattr__(key, value)

    def __getattribute__(self, key: str) -> _t.Any:
        # pylint: disable=useless-super-delegation
        # not useless; silences `mypy` with `_t.Any` and dynamic attrs
        return super().__getattribute__(key)

    def _get_key_value(
        self,
        key: str,
        kwargs: _t.Dict[str, _t.Union[bool, str]],
        default: _t.Optional[_t.Union[bool, str]] = None,
    ) -> _t.Optional[_t.Union[bool, str]]:
        return kwargs.get(key, self._kwargs.get(key, default))

    def _set_positionals(self, positionals: _t.Iterable[str]) -> None:
        for positional in positionals:
            self.__setattr__(
                positional.replace("-", "_"),
                _functools.partial(self.call, positional),
            )

    def _handle_stdout(
        self, pipe: _sp.Popen, **kwargs: _t.Union[bool, str]
    ) -> None:
        if pipe.stdout is not None:
            for line in iter(pipe.stdout.readline, b""):
                line = line.decode("utf-8", "ignore")
                file = self._get_key_value("file", kwargs)
                if file is not None:
                    with open(file, "a+", encoding="utf-8") as fout:
                        fout.write(line)
                elif self._get_key_value("capture", kwargs, False):
                    self._stdout.append(line.strip())

                elif self._get_key_value("devnull", kwargs, False):
                    with open(_os.devnull, "w", encoding="utf-8") as fout:
                        fout.write(line)

                else:
                    _sys.stdout.write(line)

    def _handle_stderr(self, pipe: _sp.Popen) -> None:
        if pipe.stderr is not None:
            for line in iter(pipe.stderr.readline, b""):
                getattr(self._logger, self._loglevel)(
                    line.decode("utf-8", "ignore").strip()
                )

    def _open_process(self, *args: str, **kwargs: _t.Union[bool, str]) -> int:
        cmd = [self._cmd, *args]
        with _sp.Popen(cmd, stdout=_sp.PIPE, stderr=_sp.PIPE) as pipe:
            self._handle_stdout(pipe, **kwargs)
            self._handle_stderr(pipe)
            return pipe.wait()

    def _sanity_check(self) -> None:
        if not _shutil.which(self._cmd):
            raise _exceptions.CommandNotFoundError(self._cmd)

    def _stringify_cmd(self, args: _t.Tuple[str, ...]) -> str:
        return f"{self._cmd} {' '.join(args)}"

    def call(self, *args: str, **kwargs: _t.Union[bool, str]) -> int:
        """Call command. Open process with ``subprocess.Popen``.

        Pipe stream depending on the keyword arguments provided to
        instance constructor or overridden through this method. If a
        file path is provided it will take precedence over the other
        options, then capture and then finally devnull. Log errors to
        file regardless. Wait for process to finish and return it's
        exit-code.

        :param args: Positional str arguments.
        :key file: File path to write stream to if not None.
        :key devnull: Send output to /dev/null.
        :key capture: Collect output array.
        :key suppress: Suppress errors and continue running.
        :raises CalledProcessError: If error occurs in subprocess.
        :return: Exit status.
        """
        self._sanity_check()
        args = tuple(str(i) for i in args)
        self._logger.debug("called with %s", args)
        returncode = self._open_process(*args, **kwargs)
        if returncode and not self._get_key_value("suppress", kwargs):
            self._logger.error("returned non-zero exit status %s", returncode)
            raise _sp.CalledProcessError(returncode, self._stringify_cmd(args))

        return returncode

    def stdout(self) -> _t.List[str]:
        """Consume accrued stdout by returning the lines of output.

        Assign new container to ``_stdout``.

        :return: List of captured stdout.
        """
        captured, self._stdout = self._stdout, []
        return captured


class Git(Subprocess):
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
