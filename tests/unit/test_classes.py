import pytest

from src import classes


@pytest.fixture
def test_api():
    example_api = classes.InfoAPI(
        endpoint="https://api.example.com",
        super_client="test_client",
        super_contact="test_contact",
    )
    return example_api


def test_api_name(test_api):
    assert test_api.name == "Generic API"


def test_api_endpoint(test_api):
    assert test_api.endpoint == "https://api.example.com"


def test_api_client(test_api):
    assert test_api.super_client == "test_client"
    assert test_api.headers["X-Super-Client"] == "test_client"


def test_api_contact(test_api):
    assert test_api.super_contact == "test_contact"
    assert test_api.headers["X-Super-Contact"] == "test_contact"


def test_api_headers(test_api):
    assert test_api.headers["accept"] == "application/json"


# TODO: Additional tests could probably be used here
# TODO: Create a mock test for the test_api() method

# TODO: Write tests for API Cache
