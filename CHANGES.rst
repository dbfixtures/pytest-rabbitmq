CHANGELOG
=========

.. towncrier release notes start

pytest-rabbitmq 4.0.0 (2026-03-22)
==================================

Breaking changes
----------------

- Converted RabbitMQ config from a TypedDict to a frozen dataclass. (`#640 <https://github.com/dbfixtures/pytest-rabbitmq/issues/640>`_)
- Drop support for Python 3.9 (`#647 <https://github.com/dbfixtures/pytest-rabbitmq/issues/647>`_)
- Drop deprecated logsdir parameter


Features
--------

- Improved xdist compatibility by introducing port-locking mechanism.

  If one worker claims a port, it locks it, and other xdist workers
  either try another port or raise a clear error message. (`#642 <https://github.com/dbfixtures/pytest-rabbitmq/issues/642>`_)
- Add `--rabbitmq-port-search-count` option - it tells how many times `pytest-rabbitmq` attempts to find unused port until it gives up.
  Useful for xdist tests. (`#642 <https://github.com/dbfixtures/pytest-rabbitmq/issues/642>`_)
- Add support for Python 3.14 (`#647 <https://github.com/dbfixtures/pytest-rabbitmq/issues/647>`_)


Bugfixes
--------

- Fix helptext for plugindir ini parameter.


Documentation
-------------

- Documented the pytest-rabbitmq plugin architecture with a new sequence diagram. (`#645 <https://github.com/dbfixtures/pytest-rabbitmq/issues/645>`_)
- Improved README onboarding and clarity: added prerequisites and a quickstart for the first test, clarified fixture cleanup behavior, and polished grammar/command consistency.


Miscellaneus
------------

- Updated workflows to actions-reuse 4.1.1 (`#621 <https://github.com/dbfixtures/pytest-rabbitmq/issues/621>`_)
- Replace black with ruff-format (`#643 <https://github.com/dbfixtures/pytest-rabbitmq/issues/643>`_)
- Add test plan testing against the oldest supported dependencies versions. (`#644 <https://github.com/dbfixtures/pytest-rabbitmq/issues/644>`_)
- Add the check-python-version-consistency pre-commit hook for pyproject.toml.

  This hook verifies that supported Python version declarations remain consistent. (`#646 <https://github.com/dbfixtures/pytest-rabbitmq/issues/646>`_)
- Add release workflow to automate release process (`#648 <https://github.com/dbfixtures/pytest-rabbitmq/issues/648>`_)
- Update pytest options to be toml native (`#664 <https://github.com/dbfixtures/pytest-rabbitmq/issues/664>`_)
- Adjust links after repository transfer
- Adjust workflows for actions-reuse 3
- Improve reliability of Coverage reporting on CI
- Install as editable package on CI, instead of import plugin to the test conftest file.
- Use pre-commit for maintaining code style and linting


3.1.1 (2024-10-15)
==================

Breaking changes
----------------

- Drop support for Python 3.8 (Already reached EOL)


Features
--------

- Declare Support for Python 3.13


3.1.0 (2024-05-08)
==================

Features
--------

- Support Python 3.12 (`#469 <https://github.com/dbfixtures/pytest-rabbitmq/issues/469>`_)


Miscellaneus
------------

- Update code formatting with black 24.1 (`#424 <https://github.com/dbfixtures/pytest-rabbitmq/issues/424>`_)
- Drop Pipfile.lock from repository - rely on a cached/artifacted one. (`#468 <https://github.com/dbfixtures/pytest-rabbitmq/issues/468>`_)


3.0.2 (2023-07-05)
==================

Bugfixes
--------

- Fixes logdir config option reading. (`#354 <https://github.com/dbfixtures/pytest-rabbitmq/issues/354>`_)
- Fixes type hints for specifying ports in Rabbitmq startup process. (`#355 <https://github.com/dbfixtures/pytest-rabbitmq/issues/355>`_)


3.0.1 (2023-06-16)
==================

Bugfixes
--------

- Fixed rabbitmq entrypoint (`#349 <https://github.com/dbfixtures/pytest-rabbitmq/issues/349>`_)


3.0.0 (2023-06-15)
==================

Breaking changes
----------------

- Add your info here (`#313 <https://github.com/dbfixtures/pytest-rabbitmq/issues/313>`_)
- Dropped support for Python 3.7 (`#324 <https://github.com/dbfixtures/pytest-rabbitmq/issues/324>`_)


Deprecations
------------

- Deprecate `rabbitmq_logsdir` and `--rabbitmq-logsdir` config options. (`#266 <https://github.com/dbfixtures/pytest-rabbitmq/issues/266>`_)


Features
--------

- Use `tmp_path_factory` instead of gettempdir() manually.
  This will allow cleaning of a temporary files. (`#266 <https://github.com/dbfixtures/pytest-rabbitmq/issues/266>`_)
- Define RABBITMQ_DIST_PORT for rabbitmq.
  Added `--rabbitmq-distribution-port` to commandline and `rabbitmq_distribution_port` to ini configuration options.

  This will help both with macos port number limit (as by default Rabbitmk adds 20000 to the Node port to determine the port), and the port being already used error.

  This port has to be different that rabbitmq port. (`#317 <https://github.com/dbfixtures/pytest-rabbitmq/issues/317>`_)
- Use towncrier to manage changelog. Require Pull Requests to contain proper newsfragment. (`#319 <https://github.com/dbfixtures/pytest-rabbitmq/issues/319>`_)
- Introduce typing and run mypy checks (`#324 <https://github.com/dbfixtures/pytest-rabbitmq/issues/324>`_)
- Official Python 3.11 support (`#329 <https://github.com/dbfixtures/pytest-rabbitmq/issues/329>`_)


Miscellaneus
------------

- Upadte test pipeline to install fresh rabbitmq from apt. (`#280 <https://github.com/dbfixtures/pytest-rabbitmq/issues/280>`_)
- Migrate dev dependency management to pipfile (`#320 <https://github.com/dbfixtures/pytest-rabbitmq/issues/320>`_)
- Migrate automerge workflow to shared one with merger app (`#321 <https://github.com/dbfixtures/pytest-rabbitmq/issues/321>`_)
- Replace pycodestyle and pydocstyle with ruff. (`#322 <https://github.com/dbfixtures/pytest-rabbitmq/issues/322>`_)
- Move package configuration to pyproject.toml (`#323 <https://github.com/dbfixtures/pytest-rabbitmq/issues/323>`_)
- Migrate to tbump to manage package versions (`#340 <https://github.com/dbfixtures/pytest-rabbitmq/issues/340>`_)


2.2.1
=====

Bugfix
------

- require `port-for>=0.6.0` which introduced the `get_port` function

Misc
----

- updated trove classifiers - added python 3.10 and pypy

2.2.0
=====

Bugfix
------

- rely on `get_port` functionality delivered by `port_for`
- Extended range of messages for list queues output

Misc
++++

- Migrate CI to github actions
- Support only python 3.7 and up

2.1.0
=====

Feature
-------
- Allow to configure plugin's location with the use of

  * **--rabbitmq-logsdir** command line argument
  * **rabbitmq_logsdir** ini file configuration option
  * **logsdir** factory argument

2.0.1
=====

- [fix] Adjust for mirakuru 2.2.0 and up

2.0.0
=====

- [cleanup] Move more rabbitmq related logic into the executor
- [enhancements] Base environment variables support on the mirakuru functionality itself
- [feature] Drop support for python 2.7. From now on, only support python 3.6 and up

1.1.2
=====

- [fix] Fix list queues functionality

1.1.1
=====

- [enhancemet] removed path.py dependency

1.1.0
=====

- [enhancements] adjust pytest-rabbitmq to pytest 3. require pytest 3.

1.0.0
=====

- [enhancements] command line and pytest.ini options for modifying rabbitmq node name
- [enhancements] command line and pytest.ini options for modifying server exec path
- [enhancements] command line and pytest.ini options for modifying ctl exec path
- [enhancements] command line and pytest.ini options for modifying host
- [enhancements] command line and pytest.ini options for modifying port
- [enhancements] command line and pytest.ini options for modifying logs directory destination
