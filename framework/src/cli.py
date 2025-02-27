import argparse
from framework.src.plugin_manager import PluginManager

def main():
    parser = argparse.ArgumentParser(description="Knowledge Graph Toolkit CLI")
    parser.add_argument("--list-plugins", action="store_true", help="List available plugins")
    parser.add_argument("--run", type=str, help="Run a specific plugin")

    args = parser.parse_args()

    plugin_manager = PluginManager("framework/src/config.yaml")
    plugins = plugin_manager.load_plugins()

    if args.list_plugins:
        print("Available plugins:", list(plugins.keys()))

    elif args.run:
        if args.run in plugins:
            print(f"Running plugin: {args.run}")
            plugins[args.run].run()
        else:
            print(f"Plugin '{args.run}' not found.")

if __name__ == "__main__":
    main()