import pytest
from helpers import perform_cleanup


@pytest.fixture(scope="session", autouse=True)
def cleanup_couriers():
    yield
    perform_cleanup()