import pandas as pd
from framework.src.plugin_base import InputPlugin

class ExcelInput(InputPlugin):
    def load_data(self, excel_path):
        try:
            # Load the "Allowed by networkpolicies" sheet
            sheet_data = pd.read_excel(excel_path, sheet_name="Allowed by networkpolicies", header=None)

            # Extract headers
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
            print(f"Error loading Excel file {self.file_path}: {e}")
            return None

    def run(self, excel_path):
        print(f"Loading data from {excel_path}...")
        return self.load_data(excel_path)