from server.main import app
from fastapi import status
from fastapi.testclient import TestClient
from common.logger import AppLogger
import pytest
import os


client = TestClient(app)
logger = AppLogger(__name__)
logger.info(os.environ['rapid_api_secret'])


def setup():
    """Setup before tests"""
    # nothing to be done
    os.mkdir('tmp')
    os.mkdir('tmp/images')


def teardown():
    """Restore the state before setup was run"""
    # nothing to be done
    os.rmdir('tmp/images')
    os.rmdir('tmp')


@pytest.fixture()
def setup_teardown():
    """Fixture to run tests between setup and teardown"""
    setup()
    yield "Do Testing"
    teardown()


def test_edit_api():
    headers = {"X-RapidAPI-Proxy-Secret": 'test_secret'}
    response = client.get('/images/edit')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = client.get('/images/edit', headers=headers)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client.post('/images/edit', headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    file_path = 'tests/test-image-1-scenery.jpeg'
    response = client.post(
        '/images/edit',
        headers=headers,
        files={
            'file': open(file_path, 'rb')})
    logger.info(response.content)
    assert response.status_code == status.HTTP_200_OK
