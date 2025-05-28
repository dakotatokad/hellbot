import logging
import os
from datetime import UTC, datetime

from . import classes

logger = logging.getLogger(__name__)


def days_from_now(date: str) -> str:
    """
    Calculates the number of days, hours, and minutes from now until the given date.

    Args:
        date (str): A date string in ISO 8601 format (e.g., "2025-05-27T10:18:17.8695449Z")

    Returns:
        str: The time from now until the given date, formatted as "X days, Y hours, Z minutes". No trailing punctuation.
    """
    from_now = str(
            datetime.fromisoformat(date[:26]).replace(tzinfo=UTC) 
            - datetime.now(UTC)
        ).split(", ")
    
    days = from_now[0]
    clock_time = from_now[1].strip().split(":")
    hours = clock_time[0]
    minutes = clock_time[1]
    
    return f"{days}, {hours} hours, and {minutes} minutes"


def ttl_from_now(future_time:str) -> int:
    """
    Calculates the time-to-live (TTL) in seconds from now until the given future time.

    Args:
        future_time (str): A date string in ISO 8601 format (e.g., "2025-05-27T10:18:17.8695449Z")

    Returns:
        int: The TTL in seconds.
    """
    return int(
        (datetime.fromisoformat(future_time[:26]).replace(tzinfo=UTC) 
         - datetime.now(UTC)).total_seconds()
    )
    

def parse_quotes(path: str, file_name: str) -> list[str]:
    """
    Parses the quotes file and returns a list of quotes.

    Returns:
        list[str]: A list of quotes with leading and trailing whitespace removed.
    """
    # os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"
    quotes_path = os.path.join(path, file_name)
    try:
        with open(quotes_path) as file:
            quotes = file.readlines()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{quotes_path}' not found in {path}.") from e
        
    # TODO: Add warning log if file has no entries
        
    quotes = [quote.strip() for quote in quotes]
        
    return quotes


def update_assignment_cache_with_orders(
    orders: list[classes.MajorOrder], 
    cache: list[classes.MajorOrder]
    ) -> list[classes.MajorOrder]:
    
    for order in orders:
        logger.debug(
            "Major Order: %s  "
            + "Rewards Type: %s "
            + "Rewards Amount: %d "
            + "Expiration: %s"
            + order.briefing, order.reward_type, order.reward_amount, order.expiration
            )
        
        #order.ttl = utils.ttl_from_now(order.expiration)
        #logger.debug("Major Order %s TTL: %d seconds", order.briefing, order.ttl)
        
        if order in cache:
            # Update the TLL if its in the cache
            order.update_ttl_from_now()
        else:
            order.response_code = 304 # Not Modified, i.e. cached
            cache.append(order)
            logger.debug("Added new order to cache: %s", order.order_id)
        
        # Check if the order is expired
        if order.ttl <= 0:
            # If the order is expired, remove it from the cache
            cache.remove(order)
            logger.debug("Removed expired order from cache: %s", order.order_id)
            
    return cache


def orders_older_than_one_day(orders: list[classes.MajorOrder]) -> bool:
    """
    Finds the largest TTL in a list of MajorOrder objects.

    Args:
        list (list[classes.MajorOrder]): A list of MajorOrder objects.

    Returns:
        bool: True if any order in the list is older than one day, False otherwise.
    """
    
    DAY_SECONDS = 24 * 60 * 60  # Number of seconds in a day
    
    for order in orders:
        if (datetime.now(UTC) - order.last_fetched).total_seconds() > DAY_SECONDS:
            logger.debug("Order %s was last fetched more than a day ago, updating cache.", order.order_id)
            return True       
    
    return False
