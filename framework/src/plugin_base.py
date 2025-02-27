from abc import ABC, abstractmethod

class PluginBase(ABC):
    """Base class for all plugins."""

    @abstractmethod
    def run(self):
        """Execute the plugin."""
        pass

class InputPlugin(PluginBase):
    """Base class for input plugins."""

    @abstractmethod
    def load_data(self):
        """Load data from a source."""
        pass

class TransformPlugin(PluginBase):
    """Base class for transformation plugins."""

    @abstractmethod
    def process_data(self, data):
        """Transform the given data."""
        pass

class OutputPlugin(PluginBase):
    """Base class for output plugins."""

    @abstractmethod
    def save_data(self, data):
        """Save data to a destination."""
        pass