import logging
import sys
from pathlib import Path
from plugin_manager import PluginManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Framework:
    def __init__(self, plugin_name, input_path, graphdb_url, config_path):
        self.plugin_name = plugin_name
        self.input_path = input_path
        self.graphdb_url = graphdb_url
        self.plugin_manager = PluginManager(config_path)  # Use PluginManager
        self.plugin = None
        self.input_module = None
        self.transform_module = None
        self.output_module = None

    def load_plugin(self):
        """Dynamically load a plugin based on its name."""
        # Get plugins loaded by PluginManager
        plugins = self.plugin_manager.load_plugins()
        if self.plugin_name not in plugins:
            logging.error(f"Plugin '{self.plugin_name}' not found.")
            sys.exit(1)
        
        # Store the plugin instance
        self.plugin = plugins[self.plugin_name]
        logging.info(f"Loaded plugin: {self.plugin_name}")

        # Load the specific modules for input, transform, and output
        self.load_modules()

    def load_modules(self):
        """Load the input, transform, and output modules."""
        plugin_path = Path(f"plugins/{self.plugin_name}/src")
        try:
            self.input_module = self.load_module(plugin_path, "input")
            self.transform_module = self.load_module(plugin_path, "transform")
            self.output_module = self.load_module(plugin_path, "output")
        except Exception as e:
            logging.error(f"Error loading modules for plugin '{self.plugin_name}': {e}")
            sys.exit(1)

    def load_module(self, plugin_path, module_type):
        """Helper function to load input, transform, or output modules."""
        module_file = plugin_path / f"{module_type}_{self.plugin_name}.py"
        module_name = f"{module_type}_{self.plugin_name}"

        if not module_file.exists():
            logging.warning(f"{module_type.capitalize()} module missing for {self.plugin_name}")
            return None

        spec = importlib.util.spec_from_file_location(module_name, module_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_plugin(self):
        """Run the plugin pipeline (Input → Transform → Output)."""
        logging.info(f"Running plugin '{self.plugin_name}'...")

        # Step 1: Load input
        data = None
        if self.input_module and hasattr(self.input_module, "run"):
            logging.info(f"Loading input for plugin '{self.plugin_name}'...")
            data = self.input_module.run(self.input_path)

        # Step 2: Transform data
        if self.transform_module and hasattr(self.transform_module, "run"):
            logging.info(f"Transforming data for plugin '{self.plugin_name}'...")
            ttl_content = self.transform_module.run(data)
        else:
            logging.error(f"No transform module found for {self.plugin_name}")
            return

        # Step 3: Save output
        if self.output_module and hasattr(self.output_module, "run"):
            logging.info(f"Saving TTL output for plugin '{self.plugin_name}'...")
            ttl_file = self.output_module.run(ttl_content)
        else:
            logging.error(f"No output module found for {self.plugin_name}")
            return

        # Step 4: Upload to GraphDB
        if self.graphdb_url:
            from framework.src.graphdb import GraphDBUploader
            uploader = GraphDBUploader(self.graphdb_url)
            logging.info(f"Uploading '{ttl_file}' to GraphDB at {self.graphdb_url}...")
            uploader.upload_ttl(ttl_file)

        logging.info(f"Plugin '{self.plugin_name}' completed.")

    def run(self):
        self.load_plugin()
        self.run_plugin()