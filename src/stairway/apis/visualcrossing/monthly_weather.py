from typing import Dict

from requests import Session

URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/historysummary"


def get_visualcrossing_monthly_weather(
    locations: str, session: Session, api_key: str, allow_async: bool = True,
) -> Dict:
    """
    Query Visual Crossing historical weather summaries API to get monthly weather.
    """

    params = {
        "aggregateHours": 24,
        "combinationMethod": "aggregate",
        "maxStations": -1,  # -1 defaults to 3
        "maxDistance": -1,  # -1 defaults to 50,000m
        "minYear": 1990,
        "maxYear": 2020,
        "chronoUnit": "months",
        "breakBy": "self",
        "dailySummaries": False,
        "contentType": "json",
        "unitGroup": "metric",
        "locationMode": "array",  # set to 'array' when querying multiple destinations
        "key": api_key,
        "dataElements": "default",
        "locations": locations,
        "allowAsynch": allow_async,
    }

    response = session.get(url=URL, params=params)
    return response
