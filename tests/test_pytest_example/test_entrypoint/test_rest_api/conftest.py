import time

from starlette.testclient import TestClient


import pytest



def start_moto_server():
    import socket
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()

    from moto.server import ThreadedMotoServer
    server = ThreadedMotoServer(port=port)
    server.start()
    from pytest_example import config
    config.CONFIG_AWS_ENDPOINT = f'http://localhost:{port}'
    return server


@pytest.fixture(scope="session")
def rest_client():


    server = start_moto_server()
    from pytest_example.entrypoint.rest_api.app import get_app

    with TestClient(get_app()) as client:
        yield client

    server.stop()
