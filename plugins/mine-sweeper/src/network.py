import os
import pandas as pd
import requests
from datetime import datetime

# ---------------------------
# Part 1: Generate TTL from Excel
# ---------------------------

def generate_ttl_from_excel(excel_path: str, ttl_output_path: str) -> str:
    """
    Generate a TTL file from an Excel spreadsheet that defines allowed network policies.
    
    Args:
    - excel_path: Path to the Excel file containing the network policy data.
    - ttl_output_path: Path where the generated TTL file will be saved.

    Returns:
    - ttl_output_path: The path to the generated TTL file.
    """
    # Load the Excel file and extract the relevant data
    sheet_data = pd.read_excel(excel_path, sheet_name="Allowed by networkpolicies", header=None)

    # Extract target and source categories and services from the sheet
    target_categories = sheet_data.iloc[0, 2:].ffill().tolist()
    target_services = sheet_data.iloc[1, 2:].tolist()
    source_categories = sheet_data.iloc[2:, 0].ffill().tolist()
    source_services = sheet_data.iloc[2:, 1].tolist()

    # Normalize category names by replacing spaces with hyphens
    source_categories = [category.replace(" ", "-") for category in source_categories]
    target_categories = [category.replace(" ", "-") for category in target_categories]

    # Initialize lists to store edges and nodes
    edges = []
    nodes = {}

    # Iterate through the data and create edges based on the allowed connections
    for row_idx, source_service in enumerate(source_services):
        for col_idx, target_service in enumerate(target_services):
            connection_value = sheet_data.iat[row_idx + 2, col_idx + 2]

            # Only consider connections with values '1' or '2'
            if pd.notna(connection_value) and connection_value in ['1', '2']:
                pattern_type = "Pattern1" if connection_value == '1' else "Pattern2"

                # Create an edge between source and target services
                edges.append({
                    "source": source_service,
                    "target": target_service,
                    "pattern": pattern_type
                })

                # Add services to the node list with corresponding categories
                if source_service not in nodes:
                    nodes[source_service] = source_categories[row_idx]
                if target_service not in nodes:
                    nodes[target_service] = target_categories[col_idx]

    # Create TTL lines with RDF syntax
    ttl_lines = []
    ttl_lines.append('@prefix ex: <http://example.org/> .')
    ttl_lines.append('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n')

    # Add nodes (services) with RDF type categories
    for service, category in nodes.items():
        ttl_lines.append(f'ex:{service} rdf:type ex:{category} .')

    # Add edges (connections) between services
    for edge in edges:
        ttl_lines.append(f'ex:{edge["source"]} ex:{edge["pattern"]} ex:{edge["target"]} .')

    # Combine TTL lines into a single string
    ttl_content = "\n".join(ttl_lines)

    # Optionally add a timestamp comment
    ttl_content = f"# Generated on {datetime.now()}\n" + ttl_content

    # Save the TTL content to the specified output path
    with open(ttl_output_path, 'w', encoding='utf-8') as file:
        file.write(ttl_content)

    print(f"TTL file generated successfully: {ttl_output_path}")
    return ttl_output_path

# -------------------------
# Part 2: Upload TTL to GraphDB
# -------------------------

def upload_ttl_to_graphdb(ttl_file: str, graphdb_url: str) -> None:
    """
    Upload a TTL file to GraphDB using an HTTP POST request.
    
    Args:
    - ttl_file: Path to the TTL file to be uploaded.
    - graphdb_url: URL of the GraphDB repository to upload the data to.
    
    Raises:
    - requests.exceptions.RequestException: If an error occurs during the HTTP request.
    """
    # Set the appropriate headers for the request
    headers = {"Content-Type": "text/turtle"}

    # Read the TTL file content
    with open(ttl_file, 'rb') as file:
        ttl_data = file.read()

    # Make the HTTP POST request to upload the TTL data
    response = requests.post(graphdb_url, data=ttl_data, headers=headers)

    # Check the response status
    if response.status_code in (200, 201, 204):
        print("GraphDB updated successfully.")
    else:
        print(f"Error updating GraphDB (Status {response.status_code}): {response.text}")
        response.raise_for_status()  # Raise an exception if the request failed

# -------------------------
# Main Routine: Orchestrates the script
# -------------------------

def main() -> None:
    """
    Main function to orchestrate the TTL generation and upload to GraphDB.
    """
    # Path to the Excel file containing network policy data
    excel_file_path = '../data/network-policy.xlsx'
    
    # Path to save the generated TTL file
    ttl_output_path = 'graph_data.ttl'
    
    # GraphDB URL (ensure it's running and accessible)
    graphdb_url = 'http://localhost:8000/repositories/network/statements'

    try:
        # Generate TTL from the Excel file
        ttl_file = generate_ttl_from_excel(excel_file_path, ttl_output_path)
        
        # Upload the generated TTL file to GraphDB
        upload_ttl_to_graphdb(ttl_file, graphdb_url)

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the script if it's executed directly
if __name__ == "__main__":
    main()