"""Tests for RabbitMqExecutor."""

from contextlib import suppress
from pathlib import Path

import pytest
from mirakuru.exceptions import ProcessExitedWithError
from port_for import get_port
from pytest import FixtureRequest, MonkeyPatch

from pytest_rabbitmq.config import get_config
from pytest_rabbitmq.factories.executor import RabbitMqExecutor


def _executor(request: FixtureRequest, path: Path) -> RabbitMqExecutor:
    """Build an executor on random ports, storing its data under path."""
    config = get_config(request)
    port = get_port(None)
    assert port
    distribution_port = get_port(None, [port])
    assert distribution_port
    return RabbitMqExecutor(
        config.server,
        config.host,
        port,
        distribution_port,
        config.ctl,
        logpath=path / "logs",
        path=path,
        plugin_path=config.plugindir,
    )


@pytest.mark.parametrize("home", [None, ""])
def test_home_defaults_to_path(
    request: FixtureRequest, tmp_path: Path, monkeypatch: MonkeyPatch, home: str | None
) -> None:
    """HOME falls back to the executor's path when it is missing or empty."""
    if home is None:
        monkeypatch.delenv("HOME", raising=False)
    else:
        monkeypatch.setenv("HOME", home)
    executor = _executor(request, tmp_path)
    # pylint:disable=protected-access
    assert executor._envvars["HOME"] == str(tmp_path)
    # pylint:enable=protected-access


def test_home_is_kept_when_set(
    request: FixtureRequest, tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """An existing HOME is left alone."""
    monkeypatch.setenv("HOME", "/home/rabbit")
    executor = _executor(request, tmp_path)
    # pylint:disable=protected-access
    assert "HOME" not in executor._envvars
    # pylint:enable=protected-access


def test_starts_without_home(
    request: FixtureRequest, tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """RabbitMQ starts and rabbitmqctl works when HOME is not set, as under tox."""
    monkeypatch.delenv("HOME", raising=False)
    executor = _executor(request, tmp_path)
    executor.start()
    try:
        assert not executor.list_queues()
    finally:
        with suppress(ProcessExitedWithError):
            executor.stop()
