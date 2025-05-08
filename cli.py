import argparse
from logging_config import LoggingConfig 
from framework.src.core import Framework

# Configure logging
logger = LoggingConfig.setup("cli")

def main():
    parser = argparse.ArgumentParser(prog="kgtoolkit", description="Knowledge Graph Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command")

    # List plugins
    subparsers.add_parser("list-plugins", help="List all available plugins")

    # Register plugin
    register_parser = subparsers.add_parser("register-plugin", help="Register a plugin by name")
    register_parser.add_argument("plugin_name", type=str, help="Name of the plugin to register")
    register_parser.add_argument("-path", type=str, help="Optional path to plugin file")


    # Run plugin
    run_parser = subparsers.add_parser("run", help="Run a specific plugin")
    run_parser.add_argument("plugin_name", type=str, help="Name of the plugin to run")
    run_parser.add_argument("-input", type=str, required=True, help="Input file path")
    run_parser.add_argument("-graphdb", type=str, help="GraphDB endpoint URL", default="http://localhost:8000")

    args = parser.parse_args()

    # Initialize Framework only once
    framework = Framework()

    if args.command == "list-plugins":
        plugins = framework.list_plugins()
        if not plugins:
            print("No plugins available.")
        else:
            print("Available plugins:")
            for name in plugins:
                print(f"- {name}")

    elif args.command == "register-plugin":
        framework.register_plugin(args.plugin_name, args.path)

    elif args.command == "run":
        framework.run_plugin(args.plugin_name, args.input, args.graphdb)
        # framework.set_input(args.input)
        # framework.set_graphdb(args.graphdb)  # Optional
        # framework.run()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()