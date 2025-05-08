class PluginError(Exception):
    """Base class for all plugin-related errors."""
    pass

class PluginNotFoundError(PluginError):
    """Raised when a plugin is not found in the directory."""
    def __init__(self, name):
        super().__init__(f"Plugin '{name}' not found in plugin directory.")

class InvalidPluginError(PluginError):
    """Raised when a plugin is invalid (missing class or bad inheritance)."""
    def __init__(self, name):
        super().__init__(f"Plugin '{name}' is not a valid PluginBase subclass.")

class PluginAlreadyRegisteredError(PluginError):
    """Raised when attempting to re-register a plugin."""
    def __init__(self, name):
        super().__init__(f"Plugin '{name}' is already registered.")