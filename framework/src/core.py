import logging
import sys
from pathlib import Path
from framework.src.plugin_manager import PluginManager

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

    def run_plugin(self):
        """Run the plugin pipeline (Input → Transform → Output)."""
        logging.info(f"Running plugin '{self.plugin_name}'...")

        # Run the plugin's run method (which already handles input, transform, output)
        ttl_file = self.plugin.run(self.input_path)

        if ttl_file:
            logging.info(f"Plugin '{self.plugin_name}' completed. Output saved to: {ttl_file}")

            # Step 4: Upload to GraphDB
            if self.graphdb_url:
                from framework.src.graphdb import GraphDBUploader
                uploader = GraphDBUploader(self.graphdb_url)
                logging.info(f"Uploading '{ttl_file}' to GraphDB at {self.graphdb_url}...")
                uploader.upload_ttl(ttl_file)

        else:
            logging.error(f"Plugin '{self.plugin_name}' failed to process the input.")

    def run(self):
        self.load_plugin()
        self.run_plugin()