import requests
import logging
from urllib.parse import urljoin

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphDBException(Exception):
    """Custom exception for GraphDB-related errors."""
    pass

class DatabaseManager:
    def __init__(self):
        self.graphdb_url = None
        self.repository = "network"
        self.connected = False
        self.query_headers = {
            'Content-Type': 'application/sparql-query',
            'Accept': 'text/turtle'  # TTL results only
        }

    def connect(self, graphdb_url):
        """Establish a connection to the GraphDB repository."""
        self.graphdb_url = graphdb_url.rstrip('/')  # Ensure there is no trailing slash
        self.connected = True  # Mark as connected
        logger.info(f"Connected to GraphDB: {self.graphdb_url}")

    def disconnect(self):
        """Disconnect from the GraphDB repository."""
        self.connected = False
        self.graphdb_url = None
        self.repository = None
        logger.info("Disconnected from GraphDB.")

    def check_connection(self):
        """Check if the connection to GraphDB is active."""
        if not self.connected:
            raise GraphDBException("Not connected to GraphDB.")

        # Here, you could ping the repository or check for its existence
        try:
            url = urljoin(self.graphdb_url + '/', f"repositories/{self.repository}/statements")
            response = requests.get(url)
            response.raise_for_status()  # Check if the repository is reachable
            logger.info(f"Connection check successful for {self.repository}.")
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            raise GraphDBException(f"Connection check failed: {e}")

    def upload_ttl(self, ttl_file_path: str):
        """Upload a TTL file to the GraphDB repository."""
        if not self.connected:
            raise GraphDBException("Cannot upload TTL. Not connected to GraphDB.")

        try:
            with open(ttl_file_path, 'rb') as file:
                data = file.read()

            url = urljoin(self.graphdb_url + '/', f"repositories/{self.repository}/statements")
            logger.info(f"Uploading TTL file '{ttl_file_path}' to {url}")
            response = requests.post(
                url,
                data=data,
                headers={'Content-Type': 'text/turtle'}
            )
            response.raise_for_status()
            logger.info("Upload successful.")
        except Exception as e:
            logger.error(f"Failed to upload TTL: {e}")
            raise GraphDBException(str(e))

    def execute_sparql_query(self, query: str) -> str:
        """Execute a SPARQL query and return the TTL result."""
        if not self.connected:
            raise GraphDBException("Cannot execute SPARQL query. Not connected to GraphDB.")

        try:
            url = urljoin(self.graphdb_url + '/', f"repositories/{self.repository}")
            response = requests.post(url, data=query, headers=self.query_headers)
            response.raise_for_status()
            return response.text  # Always return TTL format
        except Exception as e:
            logger.error(f"SPARQL query failed: {e}")
            raise GraphDBException(str(e))

    def backup_repository(self):
        """Trigger backup of the repository."""
        if not self.connected:
            raise GraphDBException("Cannot backup repository. Not connected to GraphDB.")

        try:
            url = urljoin(self.graphdb_url + '/', f"rest/repositories/{self.repository}/backup")
            logger.info(f"Backing up repository: {self.repository}")
            response = requests.post(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise GraphDBException(str(e))

    def restore_repository(self, backup_file_path: str):
        """Restore repository from a backup ZIP file."""
        if not self.connected:
            raise GraphDBException("Cannot restore repository. Not connected to GraphDB.")

        try:
            with open(backup_file_path, 'rb') as file:
                data = file.read()

            url = urljoin(self.graphdb_url + '/', f"rest/repositories/{self.repository}/restore")
            logger.info(f"Restoring repository from backup: {backup_file_path}")
            response = requests.post(
                url,
                data=data,
                headers={'Content-Type': 'application/zip'}
            )
            response.raise_for_status()
            logger.info("Restore successful.")
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise GraphDBException(str(e))