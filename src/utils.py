import os
from datetime import datetime, timezone

def days_from_now(date: str) -> str:
    """
    Calculates the number of days, hours, and minutes from now until the given date.

    Args:
        date (str): A date string in ISO 8601 format (e.g., "2025-05-27T10:18:17.8695449Z")

    Returns:
        str: The time from now until the given date, formatted as "X days, Y hours, Z minutes". No trailing punctuation.
    """
    from_now = str(
            datetime.fromisoformat(date[:26]).replace(tzinfo=timezone.utc) 
            - datetime.now(timezone.utc)
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
        (datetime.fromisoformat(future_time[:26]).replace(tzinfo=timezone.utc) 
         - datetime.now(timezone.utc)).total_seconds()
    )
    

def parse_quotes(file_name: str) -> list[str]:
    """
    Parses the quotes file and returns a list of quotes.

    Returns:
        list[str]: A list of quotes with leading and trailing whitespace removed.
    """
    quotes_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", file_name)
    with open(quotes_path, "r") as file:
        quotes = file.readlines()
        
    quotes = [quote.strip() for quote in quotes]
        
    return quotes
