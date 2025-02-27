from framework.src.plugin_base import TransformPlugin
from datetime import datetime

class TTLTransformer(TransformPlugin):
    def process_data(self, data):
        """Convert Excel data to TTL format."""
        # Convert data (same logic as before)
        ttl_lines = [
            '@prefix ex: <http://example.org/> .',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
        ]

        # Example processing (simplified for clarity)
        ttl_lines.append(f"# Generated on {datetime.now()}")

        return "\n".join(ttl_lines)

    def run(self):
        print("Transforming data to TTL format...")