from logging_config import LoggingConfig
import sys
from framework.src.plugin_manager import PluginManager
from framework.src.install_manager import InstallManager
from framework.src.database_manager import DatabaseManager
from framework.src.exceptions import PluginError, PluginNotFoundError, InvalidPluginError

logger = LoggingConfig.setup("framework")

class Framework:
    def __init__(self):
        self._plugin_manager = PluginManager()
        self._install_manager = InstallManager()
        self._database_manager = DatabaseManager()

    def _extract_repository_from_url(self, url: str) -> str:
        """Extract the repository name from the GraphDB URL."""
        parts = url.strip('/').split('/')
        try:
            return parts[parts.index('repositories') + 1]
        except (ValueError, IndexError):
            logger.error("Invalid GraphDB URL format.")
            sys.exit(1)

    def check_and_install_deps(self):
        """Ensure that all required dependencies are available."""
        self._install_manager.resolve_deps()

    def run_plugin(self, plugin_name, input_path, graphdb_url):
        if not self._plugin_manager.is_registered(plugin_name):
            logger.warning(f"Plugin '{plugin_name}' is not registered.")
            logger.info("Attempting to register it...")
            try:
                self._plugin_manager.register_plugin(plugin_name)
            except FileNotFoundError:
                logger.error(f"Aborting..")
                return

        if not self._plugin_manager.is_loaded(plugin_name):
            logger.info(f"Loading plugin '{plugin_name}'...")
            try:
                self._plugin_manager.load_plugin(plugin_name)
            except Exception as e:
                logger.error(f"Failed to load plugin '{plugin_name}': {e}")
                return

        try:
            ttl_file = self._plugin_manager.run_plugin(plugin_name, input_path)
            if ttl_file:
                logger.info(f"Plugin '{plugin_name}' executed successfully. Output: {ttl_file}")
                #self._database_manager.connect(graphdb_url)
                #self._database_manager.upload_ttl(ttl_file)
            else:
                logger.error(f"Plugin '{plugin_name}' did not return a TTL file.")
        except Exception as e:
            logger.error(f"Error while running plugin '{plugin_name}': {e}")
        finally:
            self._plugin_manager.unload_plugin(plugin_name)
            logger.info(f"Unloaded plugin '{plugin_name}' after execution.")

    def list_plugins(self):
        return self._plugin_manager.list_available_plugins()
    
    def register_plugin(self, plugin_name: str, plugin_path: str = None):
        self._plugin_manager.register_plugin(plugin_name, plugin_path)

    def run(self):
        """Main entry point."""
        #self.check_and_install_deps()
        #self.load_plugin()
        #self.run_plugin()