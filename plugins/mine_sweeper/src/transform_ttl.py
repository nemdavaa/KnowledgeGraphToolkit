from framework.src.plugin_base import TransformPlugin
from datetime import datetime

class TTLTransformer(TransformPlugin):
    def process_data(self, data):
        """
        Convert structured Excel data into TTL format.
        """

        if not data:
            print("Error: No data received for transformation.")
            return None

        # Initialize TTL lines with the generation timestamp first
        ttl_lines = [
            f"# Generated on {datetime.now()}\n",
            '@prefix ex: <http://example.org/> .',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
        ]

        # Extract data
        source_categories = data["source_categories"]
        source_services = data["source_services"]
        target_categories = data["target_categories"]
        target_services = data["target_services"]
        matrix = data["matrix"]

        edges = []
        nodes = {}

        # Process matrix to generate nodes and edges
        for row_idx, source_service in enumerate(source_services):
            for col_idx, target_service in enumerate(target_services):
                connection_value = matrix[row_idx][col_idx]

                if connection_value in ['1', '2']:
                    pattern_type = "Pattern1" if connection_value == '1' else "Pattern2"
                    edges.append({"source": source_service, "target": target_service, "pattern": pattern_type})

                    # Store nodes with their categories
                    if source_service not in nodes:
                        nodes[source_service] = source_categories[row_idx]
                    if target_service not in nodes:
                        nodes[target_service] = target_categories[col_idx]

        # Add nodes to TTL
        for service, category in nodes.items():
            ttl_lines.append(f'ex:{service} rdf:type ex:{category} .')

        # Add edges to TTL
        for edge in edges:
            ttl_lines.append(f'ex:{edge["source"]} ex:{edge["pattern"]} ex:{edge["target"]} .')

        # Convert TTL lines to a string
        return "\n".join(ttl_lines)

    def run(self, data):
        print("Transforming data to TTL format...")
        return self.process_data(data)