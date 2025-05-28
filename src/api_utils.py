import requests

from . import classes


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
            )
        )
        
    return major_orders
        