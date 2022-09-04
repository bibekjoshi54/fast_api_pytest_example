import pytest
from starlette.testclient import TestClient


def start_moto_server():
    import socket

    _socket = socket.socket()
    _socket.bind(("", 0))
    port = _socket.getsockname()[1]
    _socket.close()

    from moto.server import ThreadedMotoServer

    server = ThreadedMotoServer(ip_address='localhost', port=port)
    server.start()
    from pytest_example import config

    config.CONFIG_AWS_ENDPOINT = f"http://localhost:{port}"
    return server


@pytest.fixture(scope="session")
def rest_client():

    server = start_moto_server()
    from pytest_example.entrypoint.rest_api.app import get_app

    with TestClient(get_app()) as client:
        yield client

    server.stop()
