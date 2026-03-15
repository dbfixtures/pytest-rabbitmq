# Copyright (C) 2014 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-rabbitmq.

# pytest-rabbitmq is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-rabbitmq is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-rabbitmq.  If not, see <http://www.gnu.org/licenses/>.
"""RabbitMQ process fixture factory."""

from pathlib import Path
from typing import (
    Callable,
    Generator,
    Iterable,
)

import pytest
from mirakuru.exceptions import ProcessExitedWithError
from port_for import PortForException, PortType, get_port
from pytest import FixtureRequest, TempPathFactory

from pytest_rabbitmq.config import RabbitMQConfig, get_config
from pytest_rabbitmq.factories.executor import RabbitMqExecutor


def _rabbit_port(
    port: PortType | None, config: RabbitMQConfig, excluded_ports: Iterable[int]
) -> int:
    """User specified port, otherwise find an unused port from config."""
    rabbit_port = get_port(port, excluded_ports) or get_port(config.port, excluded_ports)
    assert rabbit_port is not None
    return rabbit_port


def rabbitmq_proc(
    server: str | None = None,
    host: str | None = None,
    port: PortType | None = -1,
    distribution_port: PortType = -1,
    node: str | None = None,
    ctl: str | None = None,
    plugindir: Path | None = None,
) -> Callable[[FixtureRequest, TempPathFactory], Generator[RabbitMqExecutor, None, None]]:
    """Fixture factory for RabbitMQ process.

    :param server: path to rabbitmq-server command
    :param host: server host
    :param port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param distribution_port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param node: RabbitMQ node name used for setting environment
                          variable RABBITMQ_NODENAME (the default depends
                          on the port number, so multiple nodes are not
                          clustered)
    :param ctl: path to rabbitmqctl file

    :returns pytest fixture with RabbitMQ process executor
    """

    @pytest.fixture(scope="session")
    def rabbitmq_proc_fixture(
        request: FixtureRequest, tmp_path_factory: TempPathFactory
    ) -> Generator[RabbitMqExecutor, None, None]:
        """Fixture for RabbitMQ process.

        #. Get config.
        #. Make a temporary directory.
        #. Setup required environment variables:
        #.  * RABBITMQ_LOG_BASE
        #.  * RABBITMQ_MNESIA_BASE
        #.  * RABBITMQ_ENABLED_PLUGINS_FILE
        #.  * RABBITMQ_NODE_PORT
        #.  * RABBITMQ_DIST_PORT
        #.  * RABBITMQ_NODENAME
        #. Start a rabbit server
            `<http://www.rabbitmq.com/man/rabbitmq-server.1.man.html>`_
        #. Stop the rabbit server and remove temporary files after tests.
        """
        config = get_config(request)
        rabbit_ctl = ctl or config.ctl
        rabbit_server = server or config.server
        rabbit_host = host or config.host

        port_path = tmp_path_factory.getbasetemp()
        if hasattr(request.config, "workerinput"):
            port_path = tmp_path_factory.getbasetemp().parent

        n = 0
        used_ports: set[int] = set()
        while True:
            try:
                rabbit_port = _rabbit_port(port, config, used_ports)
                port_filename_path = port_path / f"rabbit-{rabbit_port}.port"
                if rabbit_port in used_ports:
                    raise PortForException(
                        f"Port {rabbit_port} already in use, "
                        f"probably by other instances of the test. "
                        f"{port_filename_path} is already used."
                    )
                used_ports.add(rabbit_port)
                with (port_filename_path).open("x") as port_file:
                    port_file.write(f"rabbit_port {rabbit_port}\n")
                break
            except FileExistsError:
                n += 1
                if n >= config.port_search_count:
                    raise PortForException(
                        f"Attempted {n} times to select ports. "
                        f"All attempted ports: {', '.join(map(str, used_ports))} are already "
                        f"in use, probably by other instances of the test."
                    ) from None

        rabbit_distribution_port = get_port(distribution_port, [rabbit_port]) or get_port(
            config.distribution_port, [rabbit_port]
        )
        assert rabbit_distribution_port
        assert rabbit_distribution_port != rabbit_port, (
            "rabbit_port and distribution_port can not be the same!"
        )

        tmpdir = tmp_path_factory.mktemp(f"pytest-rabbitmq-{request.fixturename}")

        rabbit_plugin_path = plugindir or config.plugindir

        rabbit_logpath = tmpdir / "logs"

        rabbit_executor = RabbitMqExecutor(
            rabbit_server,
            rabbit_host,
            rabbit_port,
            rabbit_distribution_port,
            rabbit_ctl,
            logpath=rabbit_logpath,
            path=tmpdir,
            plugin_path=rabbit_plugin_path,
            node_name=node or config.node,
        )

        rabbit_executor.start()
        yield rabbit_executor
        try:
            rabbit_executor.stop()
        except ProcessExitedWithError:
            pass

    return rabbitmq_proc_fixture
