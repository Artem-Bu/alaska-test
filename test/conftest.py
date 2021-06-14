from time import sleep

import docker
import pytest

@pytest.fixture
def base_url(get_docker_container):
    return 'http://127.0.0.1:8091'

@pytest.fixture
def info(base_url):
    return base_url+'/info'

@pytest.fixture
def bear(base_url):
    return base_url+'/bear'

@pytest.fixture
def get_docker_container():
    """Start docker container before test, stop after"""
    client = docker.from_env()
    container = client.containers.run("azshoo/alaska:1.0", ports={'8091': 8091}, detach=True)
    sleep(1) # waiting for the container to start
    yield
    container.stop()
    container.remove()