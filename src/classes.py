import time
from dataclasses import dataclass, field

import requests

from . import utils


@dataclass
class InfoAPI:
    """
    Establishes an API endpoint for the Helldivers 2 API.
    """

    name: str = "Generic API"
    endpoint: str = "https://api.helldivers2.dev"
    super_client: str = "Default User"
    super_contact: str = "Default Contact"
    headers: dict = field(default_factory=dict)

    def __post_init__(self):
        self.headers: dict = {
            "accept": "application/json",
            "X-Super-Client": self.super_client,
            "X-Super-Contact": self.super_contact,
        }

    def test_api(self) -> int:
        """
        Tests the API connection by sending a GET request to the endpoint.

        Returns:
            int: The HTTP status code of the response.
        """
        # TODO: Log the API connection test
        try:
            response = requests.get(self.endpoint, headers=self.headers)
            return response.status_code
        except requests.RequestException as e:
            print(f"Error connecting to API: {e}")
            return 0


@dataclass
class APICache:
    """
    Establishes a cache for the API data.
    """

    data: requests.Response
    response_code: int
    timestamp: float
    ttl: int = 600

    def get_cache(self) -> tuple[requests.Response, int]:
        """
        Gets data from the cache if it is still valid.

        Raises:
            ValueError: Raises a ValueError if the cache has not been populated yet.
            TimeoutError: Raises a TimeoutError if the cache has expired.

        Returns:
            tuple[dict, int]: A tuple containing the cached data and the HTTP response code.
        """
        # TODO: Log the cache retrieval attempt
        if self.response_code == -1:
            raise ValueError("Cache has not been populated yet.")

        if (time.time() - self.timestamp) > self.ttl:
            # TODO: Is TTL necessary, or can't i just check if today is beyond the expiration date?
            # If I just set a new expiry date, I can just check if the current time is beyond that date.
            # This would remove the need for a few TTL functions.
            raise TimeoutError

        self.response_code = 304  # Not Modified
        return self.data, self.response_code

    def set_cache(
        self, data: requests.Response, response_code: int, ttl: int = 600
    ) -> None:
        """
        Sets the cache data for a given key along with its timestamp.

        Args:
            key (str): The lookup key for the cached data.
            data (dict[str, str]): The data to be cached.
            ttl (int): The time-to-live for the cache entry in seconds. Defaults to 600 seconds.
        """
        # TODO: Log the cache setting attempt
        # TODO: Catch exceptions for setter
        self.data = data
        self.response_code = response_code
        self.timestamp = time.time()
        self.ttl = ttl


@dataclass
class MajorOrder:
    """
    Represents a Major Order in the Helldivers 2 API.
    """

    order_id: int
    briefing: str
    reward_type_index: int
    reward_amount: int
    expiration: str
    reward_type: str = field(default_factory=str)
    ttl: int = field(default_factory=int)
    response_code: int = field(default_factory=int)
    
    def __post_init__(self):
        if self.reward_type_index == -1:
            self.reward_type = "N/A"
        else:
            self.reward_type = "Medals"
            
        if self.reward_amount == -1:
            self.reward_amount = 0
            
        self.ttl = utils.ttl_from_now(self.expiration)
