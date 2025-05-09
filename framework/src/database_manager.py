import os
import requests
import logging
from urllib.parse import urljoin
from logging_config import LoggingConfig

logger = LoggingConfig.setup("database_manager")

class DatabaseManager:
    def __init__(self):
        self.graphdb_url = None
        self.connected = False
        self.query_headers = {
            'Content-Type': 'application/sparql-query',
            'Accept': 'text/turtle'  # Default to TTL results
        }

    def connect(self, graphdb_url: str):
        """
        Establish a connection to GraphDB. Does not target a specific repository.

        Args:
            graphdb_url (str): Base URL of the GraphDB server (e.g., http://localhost:7200)
        """
        self.graphdb_url = graphdb_url.rstrip('/')
        self.connected = True
        logger.info(f"Connected to GraphDB at: {self.graphdb_url}")

    def disconnect(self):
        """Clear connection details and mark disconnected."""
        self.connected = False
        self.graphdb_url = None
        logger.info("Disconnected from GraphDB.")

    def check_connection(self, repository: str):
        """
        Verify the specified repository exists and is reachable.

        Args:
            repository (str): Name of the repository to check.

        Raises:
            GraphDBException: If connection fails or repository is missing.
        """
        if not self._ensure_connected(): return False

        url = urljoin(self.graphdb_url + '/', f"repositories/{repository}/statements")

        try:
            response = requests.get(url)

            if 200 <= response.status_code < 300:
                logger.info(f"Connection to repository '{repository}' verified.")
                return True
            
            elif response.status_code == 404:
                logger.warning(f"Repository '{repository}' not found.")
                logger.info(f"Attempting to create repository '{repository}'...")
                return self._create_repository(repository)
            
            else:
                logger.error(f"Failed to access repository '{repository}'.")
                return False
            
        except Exception:
            logger.error(f"Cannot reach the GraphDB server.")
            return False
    
    def upload_file(self, file_path: str, repository: str, mime_type: str = "text/turtle") -> bool:
        """
        Upload RDF content to the specified repository.

        Args:
            file_path (str): Path to RDF file (e.g., .ttl, .rdf, .nt)
            repository (str): Target GraphDB repository.
            mime_type (str): RDF MIME type (e.g., text/turtle, application/rdf+xml)

        Raises:
            GraphDBException: If upload fails.
        """
        if not self._ensure_connected(): return False
        if not self.check_connection(repository): return False

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        try:
            with open(file_path, 'rb') as f:
                data = f.read()

            url = urljoin(self.graphdb_url + '/', f"repositories/{repository}/statements")
            logger.info(f"Uploading '{file_path}' to repository '{repository}' as {mime_type}...")

            response = requests.post(url, data=data, headers={'Content-Type': mime_type})

            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Upload successful.")
                return True
            else:
                 logger.error(f"Upload failed.")
                 return False

        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            return False

    def execute_sparql_query(self, query: str, repository: str) -> str | None:
        """
        Run a SPARQL query against the specified repository and return result.

        Args:
            query (str): SPARQL query string.
            repository (str): Target repository.

        Returns:
            str: Query result in TTL format.

        Raises:
            GraphDBException: If the query fails.
        """
        if not self._ensure_connected(): return None

        try:
            url = urljoin(self.graphdb_url + '/', f"repositories/{repository}")
            response = requests.post(url, data=query, headers=self.query_headers)
            response.raise_for_status()
            logger.info("SPARQL query executed successfully.")
            return response.text
        
        except Exception as e:
            logger.error(f"SPARQL query failed: {e}")
            return None

    def backup_repository(self, repository: str) -> dict | None:
        """
        Initiate a backup of the specified repository.

        Args:
            repository (str): Target repository to backup.

        Returns:
            dict: JSON response from GraphDB (typically contains backup file info).
        """
        if not self._ensure_connected(): return None

        try:
            url = urljoin(self.graphdb_url + '/', f"rest/repositories/{repository}/backup")
            logger.info(f"Backing up repository: {repository}")
            response = requests.post(url)
            response.raise_for_status()
            logger.info("Backup successful.")
            return response.json()
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return None

    def restore_repository(self, backup_file_path: str, repository: str) -> bool:
        """
        Restore a repository from a ZIP backup file.

        Args:
            backup_file_path (str): Path to backup ZIP file.
            repository (str): Name of the repository to restore.

        Raises:
            GraphDBException: If restoration fails.
        """
        if not self._ensure_connected(): return False

        if not os.path.exists(backup_file_path):
            logger.error(f"Backup file not found: {backup_file_path}")
            return False

        try:
            with open(backup_file_path, 'rb') as file:
                data = file.read()

            url = urljoin(self.graphdb_url + '/', f"rest/repositories/{repository}/restore")
            logger.info(f"Restoring repository '{repository}' from backup: {backup_file_path}")

            response = requests.post(url, data=data, headers={'Content-Type': 'application/zip'})

            if response.status_code >= 200 and response.status_code < 300:
                logger.info("Restore successful.")
                return True
            else:
                 logger.error(f"Restore failed with status {response.status_code}: {response.text}")
                 return False
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False

    def _create_repository(self, repository: str) -> bool:
        """
        Create a new repository with default settings if it does not exist.

        Args:
            repository (str): Name of the repository to create.

        Raises:
            GraphDBException: If creation fails.
        """
        repo_config = f"""
        #
        # Auto-generated configuration for repository: {repository}
        #
        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <Repository>
            <id>{repository}</id>
            <title>{repository}</title>
            <type>graphdb:FreeSailRepository</type>
            <params>
                <RepositoryParams xmlns="http://www.ontotext.com/trree/graphdb">
                    <param name="repositoryId">{repository}</param>
                    <param name="ruleset">owl-horst-optimized</param>
                    <param name="storage-folder">{repository}</param>
                </RepositoryParams>
            </params>
        </Repository>
        """.strip()

        url = urljoin(self.graphdb_url + '/', 'rest/repositories')
        headers = {'Content-Type': 'application/xml'}

        try:
            requests.post(url, data=repo_config.encode('utf-8'), headers=headers)
        except Exception:
            logger.error(f"Failed to create repository '{repository}'.")
            return False

        logger.info(f"Repository '{repository}' created successfully.")
        return True

    def _ensure_connected(self) -> bool:
        """Raise an exception if not connected to GraphDB."""
        if not self.connected or not self.graphdb_url:
            logger.error("Not connected to GraphDB.")
            return False
        return True