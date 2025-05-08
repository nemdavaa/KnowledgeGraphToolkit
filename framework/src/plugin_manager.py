import os
import importlib.util
from framework.src.plugin_base import PluginBase
from logging_config import LoggingConfig

logger = LoggingConfig.setup("plugin_manager")

class PluginManager:
    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = plugins_dir
        self._available_plugins = {}  # plugin_name -> path
        self._loaded_plugins = {}     # plugin_name -> instance
        self.detect_plugins()

    def detect_plugins(self):
        """Detect and register all plugins from the directory."""
        if not os.path.isdir(self.plugins_dir):
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return

        for name in os.listdir(self.plugins_dir):
            plugin_file = os.path.join(self.plugins_dir, name, "src", f"{name}.py")
            if os.path.isfile(plugin_file):
                self._available_plugins[name] = plugin_file
                logger.info(f"Detected plugin: {name}")
            else:
                logger.debug(f"Skipped '{name}' — no valid plugin file found.")

    def register_plugin(self, plugin_name: str, plugin_path: str = None):
        """Manually register a plugin by path, or auto-locate it if not given."""
        if plugin_path:
            if not os.path.isfile(plugin_path):
                logger.error(f"Plugin file not found at: {plugin_path}")
                raise FileNotFoundError(plugin_path)
            self._available_plugins[plugin_name] = plugin_path
            logger.info(f"Manually registered plugin '{plugin_name}'")
        else:
            # Try to auto-locate in plugin dir
            plugin_path = os.path.join(self.plugins_dir, plugin_name, "src", f"{plugin_name}.py")
            if not os.path.isfile(plugin_path):
                logger.error(f"Plugin '{plugin_name}' not found in {plugin_path}")
                raise FileNotFoundError(plugin_path)
            self._available_plugins[plugin_name] = plugin_path
            logger.info(f"Registered plugin '{plugin_name}'")

    def is_registered(self, plugin_name: str) -> bool:
        return plugin_name in self._available_plugins

    def is_loaded(self, plugin_name: str) -> bool:
        return plugin_name in self._loaded_plugins

    def load_plugin(self, plugin_name: str):
        if not self.is_registered(plugin_name):
            raise ValueError(f"Plugin '{plugin_name}' is not registered.")

        if self.is_loaded(plugin_name):
            return  # Already loaded

        path = self._available_plugins[plugin_name]
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            class_name = self._get_class_name(plugin_name)
            plugin_class = getattr(module, class_name)

            if not issubclass(plugin_class, PluginBase):
                raise TypeError(f"{class_name} must inherit from PluginBase.")

            self._loaded_plugins[plugin_name] = plugin_class()
            logger.info(f"Loaded plugin '{plugin_name}'")
        except Exception as e:
            logger.error(f"Failed to load plugin '{plugin_name}': {e}")
            raise

    def unload_plugin(self, plugin_name: str):
        if self.is_loaded(plugin_name):
            del self._loaded_plugins[plugin_name]
            logger.info(f"Unloaded plugin '{plugin_name}'")

    def run_plugin(self, plugin_name: str, input_path: str) -> str:
        if not self.is_loaded(plugin_name):
            raise RuntimeError(f"Plugin '{plugin_name}' is not loaded.")
        plugin = self._loaded_plugins[plugin_name]
        logger.info(f"Running plugin '{plugin_name}'...")
        return plugin.run(input_path)

    def list_available_plugins(self) -> list[str]:
        return list(self._available_plugins.keys())

    def get_plugin(self, plugin_name: str):
        if not self.is_loaded(plugin_name):
            raise RuntimeError(f"Plugin '{plugin_name}' is not loaded.")
        return self._loaded_plugins[plugin_name]

    def _get_class_name(self, plugin_name) -> str:
        # Converts "my_plugin" to "MyPlugin"
        return ''.join(part.capitalize() for part in plugin_name.split('_'))