import os
import pandas as pd
from datetime import datetime
from framework.src.plugin_base import PluginBase
from logging_config import LoggingConfig

logger = LoggingConfig.setup("mine_sweeper")

class MineSweeper(PluginBase):
    def run(self, excel_path):
        """
        Full plugin to process an Excel file, transform data, and save it in TTL format.
        
        Args:
            excel_path (str): Path to the Excel input file.
            ttl_output_path (str): Path to save the resulting TTL file.
            
        Returns:
            str: The path to the saved TTL file.
        """

        # Step 1: Load data from Excel
        data = self.load_excel_data(excel_path)
        if not data:
            logger.error(f"Failed to load data from {excel_path}. Skipping...")
            return None

        # Step 2: Transform the data to TTL format
        ttl_data = self.transform_to_ttl(data)
        if not ttl_data:
            logger.error(f"Failed to transform data from {excel_path}. Skipping...")
            return None

        # Step 3: Save TTL data to a file
        ttl_file_path = self.save_ttl_data(ttl_data, excel_path)
        return ttl_file_path

    def load_excel_data(self, excel_path: str):
        """Load the Excel data for the plugin."""
        logger.info(f"Loading Excel file '{excel_path}'...")
        try:
            # Load the "Allowed by networkpolicies" sheet
            sheet_data = pd.read_excel(excel_path, sheet_name="Allowed by networkpolicies", header=None)

            # Extract headers and clean data
            target_categories = sheet_data.iloc[0, 2:].ffill().tolist()
            target_services = sheet_data.iloc[1, 2:].tolist()
            source_categories = sheet_data.iloc[2:, 0].ffill().tolist()
            source_services = sheet_data.iloc[2:, 1].tolist()

            # Clean category names (replace spaces with hyphens)
            source_categories = [category.replace(" ", "-") for category in source_categories]
            target_categories = [category.replace(" ", "-") for category in target_categories]

            data = {
                "target_categories": target_categories,
                "target_services": target_services,
                "source_categories": source_categories,
                "source_services": source_services,
                "matrix": sheet_data.iloc[2:, 2:].values.tolist()  # Extract connection values
            }

            return data
        
        except Exception as e:
            logger.error(e)
            return None

    def transform_to_ttl(self, data):
        """Convert the Excel data into TTL format."""
        if not data:
            logger.error("No data received for transformation")
            return None

        ttl_lines = [
            f"# Generated on {datetime.now()}\n",
            '@prefix ex: <http://example.org/> .',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
        ]

        source_categories = data["source_categories"]
        source_services = data["source_services"]
        target_categories = data["target_categories"]
        target_services = data["target_services"]
        matrix = data["matrix"]

        edges = []
        nodes = {}

        for row_idx, source_service in enumerate(source_services):
            for col_idx, target_service in enumerate(target_services):
                connection_value = matrix[row_idx][col_idx]

                if connection_value in ['1', '2']:  # Pattern matching
                    pattern_type = "Pattern1" if connection_value == '1' else "Pattern2"
                    edges.append({"source": source_service, "target": target_service, "pattern": pattern_type})

                    # Store nodes with their categories
                    if source_service not in nodes:
                        nodes[source_service] = source_categories[row_idx]
                    if target_service not in nodes:
                        nodes[target_service] = target_categories[col_idx]

        # Add nodes and edges to TTL
        for service, category in nodes.items():
            ttl_lines.append(f'ex:{service} rdf:type ex:{category} .')

        for edge in edges:
            ttl_lines.append(f'ex:{edge["source"]} ex:{edge["pattern"]} ex:{edge["target"]} .')

        # Convert TTL lines to a string
        return "\n".join(ttl_lines)

    def save_ttl_data(self, ttl_data: str, output_path: str):
        """Save the transformed TTL data to a file."""
        # Create TTL file name based on the Excel file name
        ttl_filename = os.path.splitext(os.path.basename(output_path))[0] + ".ttl"
        ttl_output_path = os.path.join("plugins", "mine_sweeper", "data", ttl_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(ttl_output_path), exist_ok=True)

        # Write the TTL content to the file
        with open(ttl_output_path, "w", encoding="utf-8") as file:
            file.write(ttl_data)

        logger.info(f"TTL file saved successfully: {ttl_output_path}")
        return ttl_output_path