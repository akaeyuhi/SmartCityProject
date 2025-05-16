import logging

import requests as requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.hub_gateway import HubGateway


class HubHttpAdapter(HubGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, data: ProcessedAgentData):
        """
        Save the road data to the Hub.
        Parameters:
            data (AgentData): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        url = f"{self.api_base_url}/agent_data/"

        response = requests.post(url, data=data.model_dump_json())
        if response.status_code != 200:
            logging.info(
                f"Invalid Hub response\nData: {data.model_dump_json()}\nResponse: {response}"
            )
            return False
        return True
