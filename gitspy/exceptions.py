"""
gitspy.exceptions
=================

Exceptions for use within the module.

All exceptions made public for if they need to be reraised or excepted.

Exceptions are already built into the architecture but can be used in
new plugins as well.
"""


class NotARepositoryError(OSError):
    """Raise if there is an error related to a Git repository."""

    def __init__(self) -> None:
        super().__init__("not a git repository")


class CommandNotFoundError(OSError):
    """Raise when subprocess called is not on system."""

    def __init__(self, cmd: str) -> None:
        super().__init__(f"{cmd}: command not found...")
