import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()

super_client = os.getenv("SUPER_CLIENT")
super_contact = os.getenv("SUPER_CONTACT")

class HellDivers:
    # Leveraging https://github.com/helldivers-2/api?tab=readme-ov-file
    # Swagger: https://helldivers-2.github.io/api/openapi/swagger-ui.html
    def __init__(self):
        self.name: str = "HellDivers"
        self.endpoint: str = "https://api.helldivers2.dev"
        self.headers: dict = {
            "accept": "application/json",
            "X-Super-Client": super_client,
            "X-Super-Contact": super_contact,
        }
        self._cache: dict = {} # { key: {data, timestamp, ttl}}
        
        
    def _get_from_cache(self, key: str) -> dict[str, str] | None:
        """
        Based on a key, check if the data is in the cache. If it is, check if
        the data is still valid. If it is, return the data. If not, return None.

        Args:
            key (str): The key to check in the cached data.

        Returns:
            str | int | None: The data (either as a string or int) or nothing.
        """
        # TODO: make sure dictionary is not empty
        entry = self._cache.get(key)
        if entry:
            data, timestamp, ttl = entry
            if time.time() - timestamp < ttl:
                return data
            
        return None
    
    
    def _set_cache(self, key: str, data: dict[str, str], ttl: int = 600) -> None:
        """
        Set the cache data for a given key along with its timestamp.

        Args:
            key (str): The lookup key for the cached data.
            data (str | int): The data to be cached.
            ttl (int): The time-to-live for the cache entry in seconds. Defaults to 600 seconds.
        """
        self._cache[key] = (data, time.time(), ttl)
    
    
    def get_major_order(self) -> tuple[str, str, str, int]:
        """
        Gets the current Major Order.

        Returns:
            tuple[str, str, str, int]: The Major Order as
                - briefing: The briefing for the Major Order
                - rewards: The rewards for the Major Order
                - expires: The expiration time for the Major Order
                - code: The HTTP status code (200 for success, 0 for cache)
        """
        # Check if the Major Order is in the cache
        cache_key = "major_order"
        cached_info = self._get_from_cache(cache_key)
        if cached_info:
            # TODO: Add info log for cache hit
            briefing = cached_info["briefing"]
            rewards = cached_info["rewards"]
            expires = cached_info["expires"]
            return briefing, rewards, expires, 0
        
        response_assignments = requests.get(f"{self.endpoint}/api/v1/assignments", headers=self.headers)
        code = response_assignments.status_code
        if code == 200:
            response = response_assignments.json()
            briefing = response[0]["briefing"]
            rewards = response[0]["reward"]["amount"]
            expires = response[0]["expiration"]
        else:
            briefing = "Error: Unable to fetch Major Order"
            rewards = "Error: Unable to fetch Major Order"
            expires = "Error: Unable to fetch Major Order"
            
        result = {
            "briefing": briefing,
            "rewards": rewards,
            "expires": expires
        }
        
        # Major orders are daily at minimum, so set ttl to 24 hours
        self._set_cache(cache_key, result, 86400) 
        
        return briefing, rewards, expires, code
    