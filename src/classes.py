from attr import dataclass
import requests
#import os
import time

#from dotenv import load_dotenv

#load_dotenv()

#super_client = os.getenv("SUPER_CLIENT")
#super_contact = os.getenv("SUPER_CONTACT")


class InfoAPI:
    """
    Establishes an API endpoint for the Helldivers 2 API.
    """
    # Leveraging https://github.com/helldivers-2/api?tab=readme-ov-file
    # Swagger: https://helldivers-2.github.io/api/openapi/swagger-ui.html
    def __init__(self, 
                 name: str = "Generic API", 
                 endpoint: str = "https://api.helldivers2.dev",
                 super_client: str = "Generic User",
                 super_contact: str = "Null",
                 ):
        self.name = name
        self.endpoint = endpoint
        self.api_client: str = super_client
        self.api_contact: str = super_contact
        self.headers: dict = {
            "accept": "application/json",
            "X-Super-Client": self.api_client,
            "X-Super-Contact": self.api_contact,
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
            
        self.response_code = 304 # Not Modified
        return self.data, self.response_code
            
    
    def set_cache(self, data: requests.Response, response_code: int, ttl: int = 600) -> None:
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

# class HellDivers:

#     def __init__(self):
#         self.name: str = "HellDivers"
#         self.endpoint: str = "https://api.helldivers2.dev"
#         self.headers: dict = {
#             "accept": "application/json",
#             "X-Super-Client": super_client,
#             "X-Super-Contact": super_contact,
#         }
#         self._cache: dict = {} # { key: {data, timestamp, ttl}}
        
        
#     def _get_from_cache(self, key: str) -> dict[str, str] | None:
#         """
#         Based on a key, check if the data is in the cache. If it is, check if
#         the data is still valid. If it is, return the data. If not, return None.

#         Args:
#             key (str): The key to check in the cached data.

#         Returns:
#             str | int | None: The data (either as a string or int) or nothing.
#         """
#         # TODO: make sure dictionary is not empty
#         entry = self._cache.get(key)
#         if entry:
#             data, timestamp, ttl = entry
#             if time.time() - timestamp < ttl:
#                 return data
            
#         return None
    
    
#     def _set_cache(self, key: str, data: dict[str, str], ttl: int = 600) -> None:
#         """
#         Set the cache data for a given key along with its timestamp.

#         Args:
#             key (str): The lookup key for the cached data.
#             data (str | int): The data to be cached.
#             ttl (int): The time-to-live for the cache entry in seconds. Defaults to 600 seconds.
#         """
#         self._cache[key] = (data, time.time(), ttl)
    
    
#     def get_major_order(self) -> tuple[str, str, str, int]:
#         """
#         Gets the current Major Order.

#         Returns:
#             tuple[str, str, str, int]: The Major Order as
#                 - briefing: The briefing for the Major Order
#                 - rewards: The rewards for the Major Order
#                 - expires: The expiration time for the Major Order
#                 - code: The HTTP status code (200 for success, 0 for cache)
#         """
#         # Check if the Major Order is in the cache
#         cache_key = "major_order"
#         cached_info = self._get_from_cache(cache_key)
#         if cached_info:
#             # TODO: Add info log for cache hit
#             briefing = cached_info["briefing"]
#             rewards = cached_info["rewards"]
#             expires = cached_info["expires"]
#             return briefing, rewards, expires, 0
        
#         response_assignments = requests.get(f"{self.endpoint}/api/v1/assignments", headers=self.headers)
#         code = response_assignments.status_code
#         if code == 200:
#             response = response_assignments.json()
#             briefing = response[0]["briefing"]
#             rewards = response[0]["reward"]["amount"]
#             expires = response[0]["expiration"]
#         else:
#             briefing = "Error: Unable to fetch Major Order"
#             rewards = "Error: Unable to fetch Major Order"
#             expires = "Error: Unable to fetch Major Order"
            
#         result = {
#             "briefing": briefing,
#             "rewards": rewards,
#             "expires": expires
#         }
        
#         # Major orders are daily at minimum, so set ttl to 24 hours
#         self._set_cache(cache_key, result, 86400) 
        
#         return briefing, rewards, expires, code
    