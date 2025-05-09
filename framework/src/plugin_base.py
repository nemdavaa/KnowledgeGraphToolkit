from abc import ABC, abstractmethod

class PluginBase(ABC):
    """
    Abstract base class for all plugins in the framework.

    This class defines the required interface that all plugins must implement.
    Additionally, it supports optional dependency injection for shared components
    such as the database manager.
    """

    def __init__(self):
        self.database_manager = None

    def set_managers(self, *, database_manager=None):
        """
        Inject external shared managers (e.g., DatabaseManager) into the plugin instance.

        Args:
            database_manager (DatabaseManager, optional): Instance of a database manager
                that allows the plugin to interact with a backend repository.
        """
        self.database_manager = database_manager

    @abstractmethod
    def run(self, params: dict) -> str:
        """
        Execute the plugin logic using the provided parameters.

        Args:
            params (dict): Runtime parameters for the plugin execution.

        Returns:
            str: Path to the generated output, or another result depending on the plugin.
        """
        pass

    @abstractmethod
    def info(self) -> dict:
        """
        Describe the plugin’s metadata, functionality, and expected input parameters.

        Returns:
            dict: Structured metadata including:
                - name (str): Unique plugin identifier
                - description (str): Summary of plugin behavior
                - parameters (dict): Expected input parameters with the following structure:
                    {
                        param_name: {
                            "type": str,
                            "required": bool,
                            "default": Any,
                            "description": str
                        }, ...
                    }
        """
        pass