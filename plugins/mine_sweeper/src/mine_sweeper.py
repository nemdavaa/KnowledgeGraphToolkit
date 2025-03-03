from plugins.mine_sweeper.src.input_excel import ExcelInput
from plugins.mine_sweeper.src.transform_ttl import TTLTransformer
from plugins.mine_sweeper.src.output_ttl import TTLOutput

class MineSweeper:
    def __init__(self):
        pass  # No need for initialization, everything happens in `run()`

    def run(self, excel_path):
        """
        Process an Excel file: extract data, transform to TTL, and save it.
        """

        # Step 1: Load data from Excel
        excel_input = ExcelInput()
        data = excel_input.load_data(excel_path)

        if not data:
            print(f"Error: Failed to load data from {excel_path}. Skipping...")
            return None

        # Step 2: Transform data to TTL format
        ttl_transformer = TTLTransformer()
        ttl_data = ttl_transformer.process_data(data)

        if not ttl_data:
            print(f"Error: Failed to transform data from {excel_path}. Skipping...")
            return None

        # Step 3: Save TTL data
        ttl_output = TTLOutput()
        ttl_file_path = ttl_output.save_data(ttl_data, excel_path)  # Save the TTL file and return its path

        return ttl_file_path  # The framework will handle the upload