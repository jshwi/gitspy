Status: Archived
==================
This repository has been archived and is no longer maintained

Use ``gitpython`` instead

gitspy
======
.. image:: https://img.shields.io/badge/status-inactive-red.svg
    :target: https://img.shields.io/badge/status-inactive-red.svg
    :alt: Status Inactive
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License
.. image:: https://img.shields.io/pypi/v/gitspy
    :target: https://pypi.org/project/gitspy/
    :alt: PyPI
.. image:: https://github.com/jshwi/gitspy/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/jshwi/gitspy/actions/workflows/build.yaml
    :alt: Build
.. image:: https://github.com/jshwi/gitspy/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/jshwi/gitspy/actions/workflows/codeql-analysis.yml
    :alt: CodeQL
.. image:: https://results.pre-commit.ci/badge/github/jshwi/gitspy/master.svg
   :target: https://results.pre-commit.ci/latest/github/jshwi/gitspy/master
   :alt: pre-commit.ci status
.. image:: https://codecov.io/gh/jshwi/gitspy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jshwi/gitspy
    :alt: codecov.io
.. image:: https://readthedocs.org/projects/gitspy/badge/?version=latest
    :target: https://gitspy.readthedocs.io/en/latest/?badge=latest
    :alt: readthedocs.org
.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380
    :alt: python3.8
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort
.. image:: https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg
    :target: https://github.com/PyCQA/docformatter
    :alt: docformatter
.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/PyCQA/pylint
    :alt: pylint
.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status
.. image:: https://snyk.io/test/github/jshwi/gitspy/badge.svg
    :target: https://snyk.io/test/github/jshwi/gitspy/badge.svg
    :alt: Known Vulnerabilities
.. image:: https://snyk.io/advisor/python/gitspy/badge.svg
    :target: https://snyk.io/advisor/python/gitspy
    :alt: gitspy

Intuitive Git for Python
------------------------


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
