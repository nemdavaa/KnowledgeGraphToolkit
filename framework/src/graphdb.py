import requests

def upload_ttl_to_graphdb(ttl_file: str, graphdb_url: str) -> None:
    """
    Uploads a TTL file to GraphDB via an HTTP POST request.
    
    Args:
    - ttl_file: Path to the TTL file.
    - graphdb_url: URL of the GraphDB repository where data is to be uploaded.
    """
    headers = {"Content-Type": "text/turtle"}
    
    with open(ttl_file, 'rb') as file:
        ttl_data = file.read()
    
    response = requests.post(graphdb_url, data=ttl_data, headers=headers)
    
    if response.status_code in (200, 201, 204):
        print("Successfully uploaded TTL to GraphDB.")
    else:
        print(f"Error uploading TTL: {response.status_code} {response.text}")
