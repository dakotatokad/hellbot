import pytest

from src import utils
from datetime import datetime, timedelta, timezone


@pytest.fixture
def test_string_data():
    return utils.parse_quotes("tests/test_data", "test_strings.txt")


def test_parse_quotes_returns_list(test_string_data):
    assert isinstance(test_string_data, list)


def test_parse_quotes_non_empty(test_string_data):
    assert len(test_string_data) > 0


def test_parse_quotes_strings(test_string_data):
    assert all(isinstance(quote, str) for quote in test_string_data)


def test_parse_quotes_no_empty_strings(test_string_data):
    assert all(quote.strip() for quote in test_string_data)


def test_parse_quotes_empty_file():
    with pytest.raises(FileNotFoundError):
        utils.parse_quotes("tests/test_data", "non_existent_file.txt")


def test_parse_quotes_expected_return(test_string_data):
    expected_return_index_zero = (
        "The only way to do great work is to love what you do. - Steve Jobs"
    )
    assert test_string_data[0] == expected_return_index_zero


def iso8601(dt):
    # Return ISO 8601 string with microseconds and 'Z'
    return dt.replace(tzinfo=timezone.utc).isoformat(timespec="microseconds") + "Z"


@pytest.mark.parametrize(
    "delta,expected_min",
    [
        (timedelta(seconds=5), 4),  # allow for execution delay
        (timedelta(seconds=0), -1),  # allow for execution delay
        (timedelta(days=1), 23 * 3600),  # at least 23 hours in seconds
    ],
)
def test_ttl_from_now_future_and_now(delta, expected_min):
    now = datetime.now(timezone.utc)
    future = now + delta
    future_str = iso8601(future)
    ttl = utils.ttl_from_now(future_str)
    assert ttl >= expected_min


def test_ttl_from_now_past():
    now = datetime.now(timezone.utc)
    past = now - timedelta(seconds=10)
    past_str = iso8601(past)
    ttl = utils.ttl_from_now(past_str)
    assert ttl < 0


def test_ttl_from_now_invalid_format():
    with pytest.raises(ValueError):
        utils.ttl_from_now("not-a-date")


def test_ttl_from_now_exact_now():
    now = datetime.now(timezone.utc)
    now_str = iso8601(now)
    ttl = utils.ttl_from_now(now_str)
    # Should be very close to zero
    assert abs(ttl) < 2


def test_days_from_now_invalid_format():
    with pytest.raises(ValueError):
        utils.days_from_now("bad-date-format")
