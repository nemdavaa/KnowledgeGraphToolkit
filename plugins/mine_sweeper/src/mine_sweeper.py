import os
import pandas as pd
from datetime import datetime
from framework.src.plugin_base import PluginBase
from logging_config import LoggingConfig

logger = LoggingConfig.setup("mine_sweeper")

class MineSweeper(PluginBase):
    def info(self):
        return {
            "name": "mine_sweeper",
            "description": "Processes an Excel matrix and generates TTL for network policy relationships.",
            "parameters": {
                "input": {
                    "type": "file | directory",
                    "required": False,
                    "default" : "plugins/mine_sweeper/data",
                    "description": "Path to an Excel file or directory containing Excel files."
                },
                "repository": {
                    "type": "string",
                    "required": False,
                    "default": "network",
                    "description": "GraphDB repository name for uploading TTL files."
                }
            }
        }

    def run(self, params: dict):
        input_path = params.get("input")
        repository = params.get("repository", "network")

        # Fallback to plugin's data folder if input not given
        if not input_path:
            plugin_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            input_path = os.path.join(plugin_root, "data")
            logger.info(f"No input specified. Using default data directory: {input_path}")

        if not os.path.exists(input_path):
            logger.error(f"Input path does not exist: {input_path}")

        ttl_files = []

        if os.path.isdir(input_path):
            # Process all Excel files in the directory
            for fname in os.listdir(input_path):
                if fname.endswith(".xlsx"):
                    full_path = os.path.join(input_path, fname)
                    ttl_path = self._process_excel(full_path)
                    if ttl_path:
                        ttl_files.append(ttl_path)
        elif input_path.endswith(".xlsx"):
            ttl_path = self._process_excel(input_path)
            if ttl_path:
                ttl_files.append(ttl_path)
        else:
            logger.error("Invalid input file format. Only .xlsx supported.")

        logger.info(f"Generated TTL files: {ttl_files}")
        
        # Upload each TTL file to GraphDB
        if not ttl_files:
            logger.warning("No TTL files were generated.")

        uploaded = []
        for ttl_file in ttl_files:
            success = self.database_manager.upload_file(ttl_file, repository)
            if success:
                uploaded.append(ttl_file)
            else:
                logger.error(f"Failed to upload TTL file: {ttl_file}")

        logger.info(f"Uploaded TTL files: {uploaded}")
        return uploaded

    def _process_excel(self, excel_path):
        logger.info(f"Processing Excel file: {excel_path}")
        data = self.load_excel_data(excel_path)
        if not data:
            logger.error(f"Failed to load data from {excel_path}. Skipping...")
            return None

        ttl_data = self.transform_to_ttl(data)
        if not ttl_data:
            logger.error(f"Failed to transform data from {excel_path}. Skipping...")
            return None

        return self.save_ttl_data(ttl_data, excel_path)

    def load_excel_data(self, excel_path: str):
        logger.info(f"Loading Excel file '{excel_path}'...")
        try:
            sheet_data = pd.read_excel(excel_path, sheet_name="Allowed by networkpolicies", header=None)

            target_categories = sheet_data.iloc[0, 2:].ffill().tolist()
            target_services = sheet_data.iloc[1, 2:].tolist()
            source_categories = sheet_data.iloc[2:, 0].ffill().tolist()
            source_services = sheet_data.iloc[2:, 1].tolist()

            source_categories = [category.replace(" ", "-") for category in source_categories]
            target_categories = [category.replace(" ", "-") for category in target_categories]

            return {
                "target_categories": target_categories,
                "target_services": target_services,
                "source_categories": source_categories,
                "source_services": source_services,
                "matrix": sheet_data.iloc[2:, 2:].values.tolist()
            }

        except Exception as e:
            logger.error(f"Error loading Excel file {excel_path}: {e}")
            return None

    def transform_to_ttl(self, data):
        if not data:
            logger.error("No data received for transformation")
            return None

        ttl_lines = [
            f"# Generated on {datetime.now()}\n",
            '@prefix ex: <http://example.org/> .',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
        ]

        nodes = {}
        edges = []

        for row_idx, source_service in enumerate(data["source_services"]):
            for col_idx, target_service in enumerate(data["target_services"]):
                connection_value = data["matrix"][row_idx][col_idx]

                if connection_value in ['1', '2']:
                    pattern_type = "Pattern1" if connection_value == '1' else "Pattern2"
                    edges.append({
                        "source": source_service,
                        "target": target_service,
                        "pattern": pattern_type
                    })

                    if source_service not in nodes:
                        nodes[source_service] = data["source_categories"][row_idx]
                    if target_service not in nodes:
                        nodes[target_service] = data["target_categories"][col_idx]

        for service, category in nodes.items():
            ttl_lines.append(f'ex:{service} rdf:type ex:{category} .')

        for edge in edges:
            ttl_lines.append(f'ex:{edge["source"]} ex:{edge["pattern"]} ex:{edge["target"]} .')

        return "\n".join(ttl_lines)

    def save_ttl_data(self, ttl_data: str, source_path: str):
        ttl_filename = os.path.splitext(os.path.basename(source_path))[0] + ".ttl"
        ttl_output_path = os.path.join("plugins", "mine_sweeper", "data", ttl_filename)
        os.makedirs(os.path.dirname(ttl_output_path), exist_ok=True)

        with open(ttl_output_path, "w", encoding="utf-8") as file:
            file.write(ttl_data)

        logger.info(f"TTL file saved successfully: {ttl_output_path}")
        return ttl_output_path