import os
import pandas as pd
import requests
from datetime import datetime

def generate_ttl_from_excel(excel_path: str, ttl_output_path: str) -> str:
    """
    Generate a TTL file from an Excel spreadsheet that defines allowed network policies.
    """
    sheet_data = pd.read_excel(excel_path, sheet_name="Allowed by networkpolicies", header=None)

    target_categories = sheet_data.iloc[0, 2:].ffill().tolist()
    target_services = sheet_data.iloc[1, 2:].tolist()
    source_categories = sheet_data.iloc[2:, 0].ffill().tolist()
    source_services = sheet_data.iloc[2:, 1].tolist()

    source_categories = [category.replace(" ", "-") for category in source_categories]
    target_categories = [category.replace(" ", "-") for category in target_categories]

    edges = []
    nodes = {}

    for row_idx, source_service in enumerate(source_services):
        for col_idx, target_service in enumerate(target_services):
            connection_value = sheet_data.iat[row_idx + 2, col_idx + 2]

            if pd.notna(connection_value) and connection_value in ['1', '2']:
                pattern_type = "Pattern1" if connection_value == '1' else "Pattern2"
                edges.append({"source": source_service, "target": target_service, "pattern": pattern_type})

                if source_service not in nodes:
                    nodes[source_service] = source_categories[row_idx]
                if target_service not in nodes:
                    nodes[target_service] = target_categories[col_idx]

    ttl_lines = [
        '@prefix ex: <http://example.org/> .',
        '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
    ]

    for service, category in nodes.items():
        ttl_lines.append(f'ex:{service} rdf:type ex:{category} .')

    for edge in edges:
        ttl_lines.append(f'ex:{edge["source"]} ex:{edge["pattern"]} ex:{edge["target"]} .')

    ttl_content = f"# Generated on {datetime.now()}\n" + "\n".join(ttl_lines)

    with open(ttl_output_path, 'w', encoding='utf-8') as file:
        file.write(ttl_content)

    print(f"TTL file generated successfully: {ttl_output_path}")
    return ttl_output_path

def upload_ttl_to_graphdb(ttl_file: str, graphdb_url: str) -> None:
    """
    Upload a TTL file to GraphDB using an HTTP POST request.
    """
    headers = {"Content-Type": "text/turtle"}
    with open(ttl_file, 'rb') as file:
        ttl_data = file.read()

    response = requests.post(graphdb_url, data=ttl_data, headers=headers)

    if response.status_code in (200, 201, 204):
        print("GraphDB updated successfully.")
    else:
        print(f"Error updating GraphDB (Status {response.status_code}): {response.text}")
        response.raise_for_status()

def run():
    """
    Plugin entry point.
    """
    print("Running Mine Sweeper Plugin...")
    
    excel_file_path = "plugins/mine-sweeper/data/network-policy.xlsx"
    ttl_output_path = "plugins/mine-sweeper/data/graph_data.ttl"
    graphdb_url = "http://localhost:8000/repositories/network/statements"

    try:
        ttl_file = generate_ttl_from_excel(excel_file_path, ttl_output_path)
        upload_ttl_to_graphdb(ttl_file, graphdb_url)
    except Exception as e:
        print(f"An error occurred: {e}")