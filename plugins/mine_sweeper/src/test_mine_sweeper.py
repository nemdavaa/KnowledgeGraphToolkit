from plugins.mine_sweeper.src.mine_sweeper import MineSweeper
from framework.src.database_manager import DatabaseManager
from framework.src.get_graphdb_url import get_graphdb_url

import os

print("Current Working Directory: ", os.getcwd())

# Get the actual GraphDB URL
graphdb_url = get_graphdb_url()

# Create an instance of the DatabaseManager and the plugin
db = DatabaseManager()
mine_sweeper = MineSweeper()

# Inject dependencies and connect the database
mine_sweeper.set_managers(database_manager=db)
db.connect(graphdb_url)

# Run the plugin, including upload to GraphDB
ttl_files_uploaded = mine_sweeper.run({})

# Output results
if ttl_files_uploaded:
    print(f"Test completed! TTL files uploaded: {ttl_files_uploaded}")
else:
    print("Test failed.")