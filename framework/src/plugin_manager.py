import importlib.util
import os
import yaml
from framework.src.plugin_base import PluginBase

class PluginManager:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.plugin_dir = self.config["plugins"]["path"]
        self.enabled_plugins = self.config["plugins"]["enabled"]

    def load_plugins(self):
        """Dynamically load enabled plugins."""
        plugins = {}
        for plugin_name in self.enabled_plugins:
            plugin_path = os.path.join(self.plugin_dir, f"{plugin_name}/src/{plugin_name}.py")
            if os.path.exists(plugin_path):
                module = self.load_module(plugin_name, plugin_path)
                if module:
                    plugins[plugin_name] = module
            else:
                print(f"Warning: Plugin '{plugin_name}' not found.")
        return plugins

    def load_module(self, name, path):
        """Load a Python module dynamically."""
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Ensure the module has a `run()` method and is a valid plugin
        if hasattr(module, 'run') and callable(module.run):
            return module
        else:
            print(f"Error: Plugin '{name}' does not implement a valid run() method.")
            return None