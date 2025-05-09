import yaml
import os
from logging_config import logging

logger = logging.getLogger("docker_compose_parser")

def get_graphdb_url(compose_file_path="graphdb/docker-compose.yml"):
    """
    Extract the URL for GraphDB from the docker-compose.yml file.
    
    Args:
        compose_file_path (str): Path to the docker-compose.yml file. Defaults to "docker-compose.yml".

    Returns:
        str: The GraphDB base URL, including the port.
    """
    if not os.path.exists(compose_file_path):
        logger.error(f"docker-compose.yml file not found at {compose_file_path}")
        return None

    try:
        with open(compose_file_path, 'r') as file:
            compose_data = yaml.safe_load(file)

        # Extract the GraphDB service configuration
        graphdb_service = compose_data.get('services', {}).get('graphdb', None)

        if not graphdb_service:
            logger.error("GraphDB service not found in docker-compose.yml")
            return None

        # Extract the ports to get the external URL (host:port)
        ports = graphdb_service.get('ports', [])
        if not ports:
            logger.error("No ports found for the GraphDB service in docker-compose.yml")
            return None

        # The first port binding in the format 'host_port:container_port'
        host_port = ports[0].split(':')[0]
        graphdb_url = f"http://localhost:{host_port}"

        logger.info(f"GraphDB URL extracted from docker-compose.yml: {graphdb_url}")
        return graphdb_url

    except Exception as e:
        logger.error(f"Failed to extract GraphDB URL: {e}")
        return None
