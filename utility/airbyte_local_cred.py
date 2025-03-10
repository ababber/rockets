import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# base url for airbyte instance on port 8000
AIRBYTE_API_URL = "http://localhost:8000/api/v1"

USERNAME = os.getenv("AIRBYTE_LOCAL_USER")
PASSWORD = os.getenv("AIRBYTE_LOCAL_PW")

headers = {"Content-Type": "application/json"}

# create an output directory for the responses if it doesn't exist
output_dir = "airbyte_responses"
os.makedirs(output_dir, exist_ok=True)

# list all workspaces using http basic auth 
workspace_response = requests.post(
    f"{AIRBYTE_API_URL}/workspaces/list", auth=(USERNAME, PASSWORD), headers=headers
)
workspace_json = workspace_response.json()
with open(os.path.join(output_dir, "workspaces.json"), "w") as f:
    json.dump(workspace_json, f, indent=2)
print("Workspaces saved to airbyte_responses/workspaces.json")

# list all source definitions
source_defs_response = requests.post(
    f"{AIRBYTE_API_URL}/source_definitions/list",
    auth=(USERNAME, PASSWORD),
    headers=headers,
)
source_defs_json = source_defs_response.json()
with open(os.path.join(output_dir, "source_definitions.json"), "w") as f:
    json.dump(source_defs_json, f, indent=2)
print("Source definitions saved to airbyte_responses/source_definitions.json")

# list all destination definitions
dest_defs_response = requests.post(
    f"{AIRBYTE_API_URL}/destination_definitions/list",
    auth=(USERNAME, PASSWORD),
    headers=headers,
)
dest_defs_json = dest_defs_response.json()
with open(os.path.join(output_dir, "destination_definitions.json"), "w") as f:
    json.dump(dest_defs_json, f, indent=2)
print("Destination definitions saved to airbyte_responses/destination_definitions.json")

