import pandas as pd
from framework.src.plugin_base import InputPlugin

class ExcelInput(InputPlugin):
    def __init__(self, excel_path):
        self.excel_path = excel_path

    def load_data(self):
        return pd.read_excel(self.excel_path, sheet_name="Allowed by networkpolicies", header=None)

    def run(self):
        """For debugging purposes."""
        data = self.load_data()
        print("Loaded data:", data.head())