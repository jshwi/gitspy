gitspy
======
.. image:: https://github.com/jshwi/gitspy/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/gitspy/actions/workflows/ci.yml
    :alt: ci
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/pypi/v/gitspy
    :target: https://img.shields.io/pypi/v/gitspy
    :alt: pypi
.. image:: https://codecov.io/gh/jshwi/gitspy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/gitspy
    :alt: codecov.io
.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: mit
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

Intuitive Git for Python


Install
-------
Dependencies: git ^2.0.0 (tested)

``pip install gitspy``

Development

``poetry install``

Example Usage
-------------

Get branch

.. code-block:: python

    >>> import gitspy
    >>> git = gitspy.Git()
    >>> # capture will store stdout, which can then be consumed by
    >>> # calling `git.stdout()`
    >>> # default is to print stdout, and stderr, to console
    >>> returncode = git.init(capture=True)
    >>> print(returncode)  # printing returncode
    0
    >>> # consume stdout (a list containing a `str`)
    >>> stdout = git.stdout()  # -> ['...']
    >>> items = len(stdout)  # printing length of `stdout()` outputs
    >>> print(items)
    1
    >>> # no commands have been called yet since last call to `stdout`,
    >>> # so stdout is empty
    >>> stdout = git.stdout()  # -> []
    >>> items = len(stdout)  # printing length of ``stdout()`` outputs
    >>> print(items)
    0
    >>> # stdout can be accrued
    >>> git.init(capture=True)  # ['...']
    >>> git.init(capture=True)  # ['...', '...']
    >>> print(len(git.stdout()))
    2
    >>> # stdout is consumed
    >>> print(len(git.stdout()))
    0
    >>> git.init(capture=True)
    >>> git.stdout()  # [...] -> void; clear stdout, if it exists
    >>> print(len(git.stdout()))
    0
..

Get commit hash

.. code-block:: python

    >>> import gitspy
    >>> git = gitspy.Git()
    >>> git.rev_parse("HEAD", capture=True)
    >>> stored = git.stdout()[0]
    >>> print(len(stored))  # print the length of the unique hash
    40
..
