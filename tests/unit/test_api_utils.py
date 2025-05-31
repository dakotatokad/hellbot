import pytest

#import requests
from src import classes


@pytest.fixture
def create_test_api():
    example_api = classes.InfoAPI(
        endpoint="https://api.example.com",
        super_client="test_client",
        super_contact="test_contact",
    )
    return example_api    

# TODO: Learn how to write mock tests for API calls
