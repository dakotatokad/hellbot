import requests

class HellDivers:
    def __init__(self):
        self.name = "HellDivers"
        self.endpoint = "https://api.helldivers2.dev"
        self.headers = {
            "accept": "application/json",
            "X-Super-Client": "hellbot",
            "X-Super-Contact": "https://github.com/dakotatokad/hellbot",
        }
        # Leveraging https://github.com/helldivers-2/api?tab=readme-ov-file
        # Swagger: https://helldivers-2.github.io/api/openapi/swagger-ui.html
        
    def get_major_order(self) -> tuple[str, str, str, int]:
        """
        Gets the current Major Order.

        Returns:
            tuple[str, str, str, int]: The Major Order as
                - briefing: The briefing for the Major Order
                - rewards: The rewards for the Major Order
                - expires: The expiration time for the Major Order
                - code: The HTTP status code (200 for success)
        """
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
            
        return briefing, rewards, expires, code
    