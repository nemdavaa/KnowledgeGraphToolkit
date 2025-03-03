from plugins.mine_sweeper.src.input_excel import ExcelInput
from plugins.mine_sweeper.src.transform_ttl import TTLTransformer
from plugins.mine_sweeper.src.output_ttl import TTLOutput

# Define test Excel file path
excel_path = "plugins/mine_sweeper/data/network-policy.xlsx"

# Step 1: Read Excel Data
excel_input = ExcelInput(excel_path)
data = excel_input.run()  # Should print "Reading Excel file: sample_data.xlsx..."

# Step 2: Transform to TTL
ttl_transformer = TTLTransformer()
ttl_data = ttl_transformer.run(data)  # Should print "Transforming data to TTL format..."

# Step 3: Save TTL Output
ttl_output = TTLOutput(ttl_data, excel_path)
ttl_file_path = ttl_output.run()  # Should print "Creating sample_data.ttl..."

# Print result
print(f"\nTest completed! TTL file created: {ttl_file_path}")