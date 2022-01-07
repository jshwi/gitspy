"""
gitspy.config
=============
"""
from __future__ import annotations

import os as _os
import typing as _t


class TempEnvVar:
    """Temporarily set an environment variable for context's duration.

    Ensures the environment maintains its state.

    If key already existed, once done, change the key back to its
    original value. If key did not already exist, then delete it.

    :param kwargs: Arbitrary number of key-value pairs to alter.
    """

    def __init__(self, **kwargs: str) -> None:
        self._default = {k: _os.environ.get(k) for k in kwargs}
        _os.environ.update(kwargs)

    def __enter__(self) -> TempEnvVar:
        return self

    def __exit__(
        self, exc_type: _t.Any, exc_val: _t.Any, exc_tb: _t.Any
    ) -> None:
        for key, value in self._default.items():
            if value is None:
                try:
                    del _os.environ[key]
                except KeyError:
                    # in the case that key gets deleted within context
                    pass
            else:
                _os.environ[key] = str(self._default[key])
