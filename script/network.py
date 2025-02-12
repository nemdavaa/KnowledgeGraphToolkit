import os
import pandas as pd
import requests
from datetime import datetime

# -----------------------------
# Part 1: Excel Parsing & TTL Generation
# -----------------------------

def generate_ttl_from_excel():
    # Load data without a multi-index to simplify cell access
    file_path = r'/home/enemdav/workspace/network-policy.xlsx'
    sheet_data = pd.read_excel(file_path, sheet_name="Allowed by networkpolicies", header=None)

    # Extract category and service names for rows and columns
    target_categories = sheet_data.iloc[0, 2:].ffill().tolist()
    target_services = sheet_data.iloc[1, 2:].tolist()
    source_categories = sheet_data.iloc[2:, 0].ffill().tolist()
    source_services = sheet_data.iloc[2:, 1].tolist()

    # Replace spaces with hyphens in category names
    source_categories = [item.replace(" ", "-") for item in source_categories]
    target_categories = [item.replace(" ", "-") for item in target_categories]

    # Initialize list to store edges and nodes with categories
    edges = []
    nodes = {}

    # Populate edges and categorise nodes
    for row_idx, source_service in enumerate(source_services):
        for col_idx, target_service in enumerate(target_services):
            connection_value = sheet_data.iat[row_idx + 2, col_idx + 2]

            # Only consider cells with values '1' or '2' for the pattern
            if pd.notna(connection_value) and connection_value in ['1', '2']:
                pattern_type = "Pattern1" if connection_value == '1' else "Pattern2"

                # Add the edge to the list
                edges.append({
                    "source": source_service,
                    "target": target_service,
                    "pattern": pattern_type
                })

                # Categorise nodes (add if not already added)
                if source_service not in nodes:
                    nodes[source_service] = source_categories[row_idx]
                if target_service not in nodes:
                    nodes[target_service] = target_categories[col_idx]

    # Create TTL file for GraphDB
    ttl_lines = []

    # Define prefixes for TTL
    ttl_lines.append('@prefix ex: <http://example.org/> .')
    ttl_lines.append('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n')

    # Add nodes with categories as RDF classes
    for service, category in nodes.items():
        ttl_lines.append(f'ex:{service} rdf:type ex:{category} .')

    # Add edges as RDF triples
    for edge in edges:
        ttl_lines.append(f'ex:{edge["source"]} ex:{edge["pattern"]} ex:{edge["target"]} .')

    ttl_content = "\n".join(ttl_lines)

    # Optionally, include a timestamp comment at the top
    ttl_content = f"# Generated on {datetime.now()}\n" + ttl_content

    ttl_file = 'graph_data.ttl'
    with open(ttl_file, 'w', encoding='utf-8') as f:
        f.write(ttl_content)

    print(f"TTL file '{ttl_file}' generated successfully.")
    return ttl_file

# -----------------------------
# Part 2: Upload TTL Data to GraphDB
# -----------------------------

def upload_ttl_to_graphdb(ttl_file):
    # Update this URL with your GraphDB repository endpoint
    graphdb_url = "http://1a02ce968e8c:7200/repositories/network-test"
    headers = {"Content-Type": "text/turtle"}

    # If authentication is needed, for example:
    # auth = ('username', 'password')
    # response = requests.post(graphdb_url, data=ttl_data, headers=headers, auth=auth)

    with open(ttl_file, 'rb') as f:
        ttl_data = f.read()

    response = requests.post(graphdb_url, data=ttl_data, headers=headers)

    if response.status_code in (200, 201, 204):
        print("GraphDB updated successfully.")
    else:
        print(f"Error updating GraphDB (Status {response.status_code}): {response.text}")

# -----------------------------
# Main Routine
# -----------------------------

def main():
    ttl_file = generate_ttl_from_excel()
    upload_ttl_to_graphdb(ttl_file)

if __name__ == "__main__":
    main()