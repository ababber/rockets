# source_sportsradar_nba/streams.py
import requests
from airbyte_cdk.models import SyncMode
from airbyte_cdk.sources.streams.http import HttpStream


class TeamsStream(HttpStream):

    name = "teams"

    # base for SportRadar NBA v8 trial
    url_base = "https://api.sportradar.com/nba/trial/v8/en/"
    path = "league/hierarchy.json"

    primary_key = "id"

    def __init__(self, api_key: str, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key

    def request_params(
        self, stream_slice=None, stream_state=None, next_page_token=None
    ) -> dict:
        return {"api_key": self.api_key}

    def parse_response(self, response, **kwargs):
        data = response.json()

        conferences = data.get("conferences", [])
        for conf in conferences:
            divisions = conf.get("divisions", [])
            for div in divisions:
                teams = div.get("teams", [])
                for team in teams:
                    yield team
