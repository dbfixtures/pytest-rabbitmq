"""pytest-rabbitmq configuration."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pytest import FixtureRequest


@dataclass(frozen=True)
class RabbitMQConfig:
    """Pytest RabbitMQ config definition type."""

    host: str
    port: int | None
    port_search_count: int
    distribution_port: int | None
    server: str
    ctl: str
    node: str | None
    plugindir: Path


def get_config(request: FixtureRequest) -> RabbitMQConfig:
    """Return a pytest-rabbitmq configuration."""

    def get_conf_option(option: str) -> Any:
        option_name = "rabbitmq_" + option
        return request.config.getoption(option_name) or request.config.getini(option_name)

    port = get_conf_option("port")
    distribution_port = get_conf_option("distribution_port")
    return RabbitMQConfig(
        host=get_conf_option("host"),
        port=int(port) if port else None,
        port_search_count=int(get_conf_option("port_search_count")),
        distribution_port=int(distribution_port) if distribution_port else None,
        server=get_conf_option("server"),
        ctl=get_conf_option("ctl"),
        node=get_conf_option("node"),
        plugindir=Path(get_conf_option("plugindir")),
    )
