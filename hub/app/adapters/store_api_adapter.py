import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        try:
            url = f"{self.api_base_url}/processed_agent_data"
            payload = [data.model_dump() for data in processed_agent_data_batch]

            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()

            logging.info(f"Successfully saved {len(payload)} records to {url}")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to save data to store API: {e}")
            return False
