from plugins.mine_sweeper.src.mine_sweeper import MineSweeper

import os
print("Current Working Directory: ", os.getcwd())

# Define test Excel file path (Make sure this file exists at the specified path)
excel_path = "plugins/mine_sweeper/data/network-policy.xlsx"

# Create an instance of MineSweeper and run the process
mine_sweeper = MineSweeper()

# Run the plugin, which will load data, transform it, and save the TTL output
ttl_file_path = mine_sweeper.run(excel_path)

# Final result
if ttl_file_path:
    print(f"Test completed! TTL file created at: {ttl_file_path}")
else:
    print("Test failed.")