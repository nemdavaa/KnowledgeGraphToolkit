import importlib.util
import os
import yaml

class PluginManager:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.plugin_dir = self.config["plugins"]["path"]
        self.enabled_plugins = self.config["plugins"]["enabled"]

    def load_plugins(self):
        """
        Load enabled plugins dynamically.
        """
        plugins = {}
        for plugin_name in self.enabled_plugins:
            plugin_path = os.path.join(self.plugin_dir, f"{plugin_name}.py")
            if os.path.exists(plugin_path):
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                plugins[plugin_name] = module
            else:
                print(f"Warning: Plugin '{plugin_name}' not found.")
        return plugins