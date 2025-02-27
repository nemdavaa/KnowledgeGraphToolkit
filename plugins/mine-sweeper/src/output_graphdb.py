import requests
from framework.src.plugin_base import OutputPlugin

class GraphDBOutput(OutputPlugin):
    def __init__(self, graphdb_url):
        self.graphdb_url = graphdb_url

    def save_data(self, data):
        headers = {"Content-Type": "text/turtle"}
        response = requests.post(self.graphdb_url, data=data, headers=headers)
        if response.status_code in (200, 201, 204):
            print("Successfully uploaded TTL to GraphDB.")
        else:
            print(f"Error uploading TTL: {response.status_code} {response.text}")

    def run(self):
        print("Uploading data to GraphDB...")