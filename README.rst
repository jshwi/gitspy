gitspy
======
.. image:: https://github.com/jshwi/gitspy/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/jshwi/gitspy/actions/workflows/ci.yml
    :alt: ci
.. image:: https://github.com/jshwi/gitspy/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/gitspy/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://readthedocs.org/projects/gitspy/badge/?version=latest
    :target: https://gitspy.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
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
**********

Capture will store stdout, which can then be consumed by calling `git.stdout()`

Default is to return returncode and print stdout and stderr to console

.. code-block:: python

    >>> import gitspy
    >>> git = gitspy.Git()
    >>> git.init(capture=True)  # ['...']
    0

Consume stdout (a list containing a str)

.. code-block:: python

    >>> len(git.stdout())  # []
    1

No commands have been called yet since last call to `stdout` so stdout is empty

.. code-block:: python

    >>> len(git.stdout())  # []
    0

Stdout can be accrued

.. code-block:: python

    >>> git.init(capture=True)  # ['...']
    0
    >>> git.init(capture=True)  # ['...', '...']
    0
    >>> len(git.stdout())  # []
    2

Stdout is consumed

.. code-block:: python

    >>> len(git.stdout())  # []
    0

Get commit hash
***************

.. code-block:: python

    >>> git.rev_parse("HEAD", capture=True)  # ['...']
    0
    >>> len(git.stdout()[0])  # []
    40
