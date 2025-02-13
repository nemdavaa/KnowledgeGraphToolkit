import yaml
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from framework.src.graphdb import upload_ttl_to_graphdb
from framework.src.plugin_manager import PluginManager

def load_config(config_path: str) -> dict:
    """Load YAML configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config("framework/src/config.yaml")

    # Load plugins
    plugin_manager = PluginManager("framework/src/config.yaml")
    plugins = plugin_manager.load_plugins()

    # Run each enabled plugin
    for name, plugin in plugins.items():
        print(f"Running plugin: {name}")
        plugin.run()  # Assumes each plugin has a `run()` function

    # Upload TTL to GraphDB
    upload_ttl_to_graphdb(config["graphdb"]["ttl_output"], config["graphdb"]["url"])

if __name__ == "__main__":
    main()