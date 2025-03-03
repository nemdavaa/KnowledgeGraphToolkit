import os
from framework.src.plugin_base import OutputPlugin

class TTLOutput(OutputPlugin):
    def __init__(self, ttl_data, excel_path):
        """
        Initialize with the TTL data and the original Excel file path.
        The TTL filename will be derived from the Excel filename.
        """
        self.ttl_data = ttl_data
        self.excel_path = excel_path

    def save_data(self):
        """
        Save the transformed TTL data to a file.
        """
        # Create a TTL file name based on the Excel file name
        ttl_filename = os.path.splitext(os.path.basename(self.excel_path))[0] + ".ttl"
        ttl_output_path = os.path.join("plugins", "mine_sweeper", "data", ttl_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(ttl_output_path), exist_ok=True)

        # Write the TTL content to the file
        with open(ttl_output_path, "w", encoding="utf-8") as file:
            file.write(self.ttl_data)

        print(f"TTL file saved successfully: {ttl_output_path}")
        return ttl_output_path

    def run(self):
        """
        Run the output plugin to save the TTL data.
        """
        ttl_filename = os.path.splitext(os.path.basename(self.excel_path))[0] + ".ttl"
        print(f"Creating {ttl_filename}...")
        return self.save_data()