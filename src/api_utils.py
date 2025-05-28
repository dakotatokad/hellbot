import logging
from datetime import UTC, datetime

import requests

from . import classes

logger = logging.getLogger(__name__)

async def query_api(
        api: classes.InfoAPI,  
        query: str,
        version: str = "v1",
    ) -> tuple[requests.Response, int]:
    """
    Query the API endpoint with the specified query and version.

    Args:
        api (InfoAPI): An API instance containing the endpoint and headers.
        query (str): The specific query to be made to the API, see Swagger.
        version (str, optional): The API version to utilize in the query. Defaults to "v1".

    Returns:
        tuple[dict, int]: A tuple of information
            dict: The JSON response from the API.
            int: The HTTP status code of the response.
    """
    response = requests.get(
        f"{api.endpoint}/api/{version}/{query}",
        headers = api.headers
    )
        
    return response, response.status_code    
  
      
def parse_requests_data(data: requests.Response) -> list[dict]:
    """
    Parses the requests.Response data into a list or dictionary.

    Args:
        data (requests.Response): The data payload from requests.Response.

    Raises:
        TypeError: If the data is not a list or a Response object.

    Returns:
        list | dict: The parsable data as a list or dictionary.
    """
    if isinstance(data, list):
        return data
    elif hasattr(data, "json"):
        return data.json()
    else:
        raise TypeError("Data is not a list or a Response object")
    
    
def parse_major_orders(assignments: list) -> list[classes.MajorOrder]:
    """
    Parses out each of the major orders, their briefing, rewards, and expiration date.

    Args:
        assignments (list): A list of assignments from the API.

    Returns:
        list[classes.MajorOrder]: A list of MajorOrder objects containing the parsed data.
    """
    
    major_orders: list[classes.MajorOrder] = []
    
    for order in assignments:
        briefing = order["briefing"]
        id = order["id"]
        
        try:
            reward_type_index = order["rewards"][0]["type"]
        except (IndexError, KeyError):
            reward_type_index = -1
            
        try:
            reward_amount = order["rewards"][0]["amount"]
        except (IndexError, KeyError):
            reward_amount = -1
        
        expiration = order["expiration"]
        
        major_orders.append(
            classes.MajorOrder(
                order_id = id,
                briefing = briefing,
                reward_type_index = reward_type_index,
                reward_amount = reward_amount,
                expiration = expiration,
                last_fetched = datetime.now(UTC)
            )
        )
        
    return major_orders


def remove_expired_assignments(assignments: list[classes.MajorOrder]) -> list[classes.MajorOrder]:
    """
    Removes expired assignments from the list of MajorOrder objects.

    Args:
        assignments (list[classes.MajorOrder]): A list of MajorOrder objects.

    Returns:
        list[classes.MajorOrder]: A list of MajorOrder objects with expired assignments removed.
    """
    if  len(assignments) == 0:
        logger.debug("No assignments to check for expiration.")
        return assignments
    
    for assignment in assignments:
        assignment.update_ttl_from_now()
        if assignment.ttl <= 0:
            assignments.remove(assignment)
        logger.debug("Removed expired assignment: %s", assignment.order_id)
        
    return assignments


async def fetch_and_parse_from_api(
    api: classes.InfoAPI, 
    query: str, 
    version: str = "v1"
    ) -> list[dict]:
    """
    Fetches data from the specified API and parses it into a list of MajorOrder objects.

    Args:
        api (classes.InfoAPI): _description_
        query (str): _description_
        version (str, optional): _description_. Defaults to "v1".

    Raises:
        ConnectionError: _description_

    Returns:
        list[dict]: _description_
    """
    
    raw_data, response_code = await query_api(
        api = api,
        query = "assignments",
    )
    logger.debug(f"API Query: {raw_data}, Response Code: {response_code}")        

    if response_code != 200:
        logging.debug(
            "Failed to fetch data from API. "
            + "Response Code: %d", response_code
        )
        raise ConnectionError

    parsed_data = parse_requests_data(raw_data)
    logger.debug("Parsed Data: %s", parsed_data)
    
    return parsed_data
