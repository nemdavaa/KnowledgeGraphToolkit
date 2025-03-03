import argparse
import logging
from framework.src.framework import Framework
from framework.src.plugin_manager import PluginManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def list_plugins(config_path):
    """List all available plugins."""
    plugin_manager = PluginManager(config_path)
    plugins = plugin_manager.load_plugins()
    
    if not plugins:
        print("No plugins available.")
    else:
        print("Available plugins:")
        for name in plugins.keys():
            print(f"- {name}")

def run_plugin(plugin_name, input_path, graphdb_url, config_path):
    """Run a specific plugin."""
    logging.info(f"Running plugin '{plugin_name}' with input '{input_path}'...")

    framework = Framework(plugin_name, input_path, graphdb_url, config_path)
    framework.run()

    logging.info(f"Plugin '{plugin_name}' completed.")

def main():
    parser = argparse.ArgumentParser(prog="KGToolKit", description="Knowledge Graph Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command")

    # List plugins command
    list_parser = subparsers.add_parser("list-plugins", help="List all available plugins")
    list_parser.add_argument("--config", type=str, help="Path to the config file", default="framework/src/config.yaml")

    # Run plugin command
    run_parser = subparsers.add_parser("run", help="Run a specific plugin")
    run_parser.add_argument("plugin_name", type=str, help="The name of the plugin to run")
    run_parser.add_argument("--input", type=str, help="Path to input data (file or folder)", required=True)
    run_parser.add_argument("--graphdb", type=str, help="GraphDB endpoint URL", default=None)
    run_parser.add_argument("--config", type=str, help="Path to the config file", default="framework/src/config.yaml")

    args = parser.parse_args()

    if args.command == "list-plugins":
        list_plugins(args.config)
    elif args.command == "run":
        run_plugin(args.plugin_name, args.input, args.graphdb, args.config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()