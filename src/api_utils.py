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
  
      
def parse_requests_data(data: requests.Response) -> list | dict:
    """
    Parses the requests.Response data into a list or dictionary.

    Args:
        data (requests.Response): The data payload from requests.Response.

    Raises:
        TypeError: If the data is not a list or a Response object.

    Returns:
        list | dict: The parsable data as a list or dictionary.
    """
    if isinstance(data, (list | dict)):
        return data
    elif hasattr(data, "json"):
        return data.json()
    else:
        raise TypeError("Data is not a list, dict, or a Response object")
    