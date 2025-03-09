import json
from airbyte

client = AirbyteClient(host="http://localhost:8001")  # if Airbyte is running locally

# 1) Create or update the custom SportRadar NBA source definition
source_def = client.create_or_update_source_definition(
    name="SportRadar NBA",
    # Docker repository from your build or a local reference
    docker_repository="your_docker_user/source-sportsradar-nba",
    docker_image_tag="latest"
)

# 2) Create a source instance
source_config = {
    "api_key": "<YOUR_SPORTRADAR_API_KEY>"
}
source = client.create_source(
    name="SportRadar NBA Source",
    source_definition_id=source_def.source_definition_id,
    connection_configuration=source_config,
    workspace_id=client.get_workspace_id()
)

# 3) Create the Snowflake destination
with open("snowflake_destination.json") as f:
    snowflake_config = json.load(f)

destination_def_id = snowflake_config["destinationDefinitionId"]
destination_config = snowflake_config["connectionConfiguration"]

destination = client.create_destination(
    name="My Snowflake Dest",
    destination_definition_id=destination_def_id,
    connection_configuration=destination_config,
    workspace_id=client.get_workspace_id()
)

# 4) Create the connection
connection = client.create_connection(
    name="SportRadar NBA -> Snowflake",
    source_id=source.source_id,
    destination_id=destination.destination_id,
    sync_catalog=client.discover_and_select_all_fields(source.source_id),
    schedule=None  # or specify a schedule for recurring syncs
)

# 5) Run the sync
job = client.sync_connection(connection_id=connection.connection_id)
print(f"Sync job created: {job.job.id}")

# (Optional) Check job status
job_info = client.get_job_info(job.job.id)
print(job_info.status)
