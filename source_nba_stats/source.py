from typing import List
from airbyte_cdk.sources import Source
from airbyte_cdk.models import ConnectorSpecification, AirbyteConnectionStatus
from airbyte_cdk.sources.streams import Stream
from .streams import TeamsStream

class SourceSportRadarNBA(Source):
    def check_connection(self, logger, config) -> (bool, any):
        """
        Make a simple request to verify the API key works.
        """
        try:
            stream = TeamsStream(api_key=config["api_key"])
            resp = stream.requests_session.get(
                f"{stream.url_base}{stream.path}",
                params={"api_key": config["api_key"]}
            )
            if resp.status_code == 200:
                return True, None
            else:
                return False, f"Failed with status {resp.status_code}: {resp.text}"
        except Exception as e:
            return False, str(e)

    def streams(self, config: dict) -> List[Stream]:
        return [TeamsStream(api_key=config["api_key"])]

    def spec(self, *args, **kwargs) -> ConnectorSpecification:
        return ConnectorSpecification(
            documentationUrl="https://developer.sportradar.com/basketball/reference/nba-overview",
            changelogUrl="https://github.com/airbytehq/airbyte",
            connectionSpecification={
                "type": "object",
                "required": ["api_key"],
                "properties": {
                    "api_key": {
                        "type": "string",
                        "description": "Your SportRadar NBA API key"
                    }
                },
            },
        )
