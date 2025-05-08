from abc import ABC, abstractmethod

class PluginBase(ABC):
    """
    Base class for all plugins. Each plugin must implement `run` and `get_metadata`.
    """

    @abstractmethod
    def run(self, params: dict) -> str:
        """
        Run the plugin with the given parameters.
        Args:
            params (dict): Parameters for the plugin
        Returns:
            str: Output path or result.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> dict:
        """
        Return plugin metadata including expected parameters.
        Returns:
            dict: Metadata including name, description, parameters, etc.
        Example:
            {
                "name": "mine_sweeper",
                "description": "Parses mines from Excel and generates RDF.",
                "parameters": {
                    "input": {"type": "str", "required": True},
                    "repname": {"type": "str", "required": True},
                    "user": {"type": "str", "required": False, "default": None}
                }
            }
        """
        pass