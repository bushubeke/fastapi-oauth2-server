from http import client
import pytest
import asyncio

from oauth2.main import create_dev_app
pytestmark = pytest.mark.oauth_end_tests

# app=create_dev_app()

@pytest.fixture(scope="module")
def testing_client():
    app=create_dev_app()
    yield app
    
    
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

