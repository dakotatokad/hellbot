import pytest
import time
from classes import HellDivers

@pytest.fixture
def helldivers():
    return HellDivers()

def test_set_and_get_cache_valid(helldivers):
    key = "test_key"
    data = {"briefing": "Test", "rewards": "100", "expires": "soon"}
    helldivers._set_cache(key, data, ttl=2)
    result = helldivers._get_from_cache(key)
    assert result == data

def test_get_cache_expired(helldivers):
    key = "test_key"
    data = {"briefing": "Test", "rewards": "100", "expires": "soon"}
    helldivers._set_cache(key, data, ttl=1)
    time.sleep(1.1)
    result = helldivers._get_from_cache(key)
    assert result is None

def test_get_cache_missing_key(helldivers):
    result = helldivers._get_from_cache("nonexistent")
    assert result is None
