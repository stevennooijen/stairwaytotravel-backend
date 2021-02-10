import logging
import time
from typing import Dict

from requests import Session
from requests.models import Response

URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/historysummary"


def get_visualcrossing_monthly_weather(
    locations: str, session: Session, api_key: str, allow_async: bool = True,
) -> Response:
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


def await_completion(
    data: Dict, session: Session, api_key: str, seconds_between_retries: int = 5
) -> Dict:
    """
    Monitor asynchronous Visual Crossing historical weather summaries API call and return data when finished.
    """
    # if there is an errorCode we should nog proceed with this function
    if data["errorCode"] != 0:
        logging.warning(f"errorCode not 0, input response data: {data}")
        raise
    # as long as there is a status field, there is no data. So keep querying
    while "status" in data:
        # check for wrong responses
        if data["status"] in [4, 5]:
            logging.warning(f"Status 4 or 5, response data: {data}")
            raise
        if data["errorCode"] != 0:
            logging.warning(f"errorCode not 0, response data: {data}")
            raise
        if "directCallback" not in data:
            logging.warning(f"No CallBack, response data: {data}")
            raise
        # if good, sleep and retry
        time.sleep(seconds_between_retries)
        data = session.get(url=data["directCallback"], params={"key": api_key}).json()

    return data
