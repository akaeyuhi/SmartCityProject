from abc import ABC, abstractmethod
from app.entities.agent_data import AgentData


class HubGateway(ABC):
    """
    Abstract class representing the Store Gateway interface.
    All store gateway adapters must implement these methods.
    """

    @abstractmethod
    def save_data(self, data: AgentData) -> bool:
        """
        Method to save the agent data in the database.
        Parameters:
            data (AgentData): The agent data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        pass
