import importlib.util
import os
import yaml

class PluginManager:
    def __init__(self, config_path: str):
        """Initialize with configuration file path."""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.plugin_dir = self.config["plugins"]["path"]
        self.enabled_plugins = self.config["plugins"]["enabled"]

    def load_plugins(self):
        """Dynamically load enabled plugins."""
        plugins = {}
        for plugin in self.enabled_plugins:
            name = plugin['name']
            plugin_path = os.path.join(self.plugin_dir, name, 'src', f'{name}.py')
            if os.path.exists(plugin_path):
                module = self.load_module(name, plugin_path)
                if module:
                    plugin_instance = getattr(module, name.capitalize())()  # Instantiate plugin class
                    plugins[name] = plugin_instance
            else:
                print(f"Warning: Plugin '{name}' not found.")
        return plugins

    def load_module(self, name, path):
        """Load a Python module dynamically."""
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, name.capitalize()):  # Ensure class exists
            return module
        else:
            print(f"Error: Plugin '{name}' is missing the class '{name.capitalize()}'.")
            return None