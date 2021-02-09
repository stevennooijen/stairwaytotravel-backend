import logging
import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv
from stairway.apis.visualcrossing.monthly_weather import (
    get_visualcrossing_monthly_weather,
)

load_dotenv()


VISUALCROSSING_KEY = os.getenv("VISUALCROSSING_KEY")
URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/historysummary"
# Take into account Visual Crossing API maximum of 10 places in one call
STEP_SIZE = 10
SLEEP_SECONDS = 5

logging.basicConfig(level=logging.WARNING)


def main(*args):
    options = parse_args(*args)

    S = requests.Session()

    # Read and prep input df
    df_places = (
        pd.read_csv(options.input_path)
        .rename(columns={"id": "stairway_id"})
        .assign(
            location=lambda df: df["lat"].round(6).astype(str)
            + ","
            + df["lng"].round(6).astype(str)
        )[["stairway_id", "location"]]
    )

    print(f"Number of places to process: {len(df_places)}")

    # Process chuncked up input df with a sleep timer of an hour
    for i in range(int(options.start_index), len(df_places), STEP_SIZE):
        print(f"Now doing places: {i}-{i + STEP_SIZE}")
        places_chunck = df_places.iloc[i : i + STEP_SIZE]
        places_chunck = process_chunck(
            places_chunck,
            chunck_identifier=f"{i}-{i+STEP_SIZE}",
            session=S,
            api_key=VISUALCROSSING_KEY,
        )

        # if file does not exist write with header, else append
        if not os.path.isfile(options.output_path):
            places_chunck.to_csv(options.output_path, index=False)
        else:
            places_chunck.to_csv(
                options.output_path, mode="a", header=False, index=False
            )
        # print(f"Done processing places: {i}-{i + STEP_SIZE}")
        # print("Sleeping ... zzz")
        # time.sleep(SLEEP_SECONDS)

    print("Done!")


def parse_args(*args):
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Retrieve monthly weather data from Visual Crossing."
    )
    parser.add_argument(
        "-i",
        "--input-path",
        dest="input_path",
        default="data/wikivoyage/enriched/wikivoyage_destinations.csv",
        help="Path to the destinations input file.",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        default="data/visualcrossing/visualcrossing_monthly_weather.csv",
        help="Path to the output file.",
    )
    parser.add_argument(
        "-s",
        "--start-index",
        dest="start_index",
        default=0,
        help="Index of first place to start processing",
    )

    return parser.parse_args(args=args)


def create_locations_string(df):
    return "|".join(df["location"].to_list())


def await_completion(response, session):
    data = response.json()
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
        time.sleep(SLEEP_SECONDS)
        data = session.get(
            url=data["directCallback"], params={"key": VISUALCROSSING_KEY}
        ).json()

    return data


def process_chunck(df, chunck_identifier, session, api_key):
    locations = create_locations_string(df)
    try:
        # actual API call
        response = get_visualcrossing_monthly_weather(locations, session, api_key)
        data = await_completion(response, session=session)
    except:
        logging.exception(
            logging.warning(
                f"Failed at chuck {chunck_identifier} with locations string: {locations}"
            )
        )
        raise
    # filter out places with no data
    data = [place for place in data["locations"] if place["values"] is not None]
    df_weather = pd.io.json.json_normalize(data, "values", ["name", "tz"])
    # add back in the stairway id
    df_out = pd.merge(
        df, df_weather, how="inner", left_on=["location"], right_on=["name"]
    ).drop(columns=["name", "location"])
    return df_out


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
