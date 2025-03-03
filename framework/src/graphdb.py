import requests

class GraphDBUploader:
    def __init__(self, graphdb_url):
        self.graphdb_url = graphdb_url

    def upload_ttl(self, ttl_file):
        """Upload a TTL file to GraphDB."""
        headers = {"Content-Type": "text/turtle"}
        with open(ttl_file, 'rb') as file:
            ttl_data = file.read()

        response = requests.post(self.graphdb_url, data=ttl_data, headers=headers)

        if response.status_code in (200, 201, 204):
            print(f"GraphDB updated successfully with {ttl_file}.")
        else:
            print(f"Error uploading {ttl_file} (Status {response.status_code}): {response.text}")