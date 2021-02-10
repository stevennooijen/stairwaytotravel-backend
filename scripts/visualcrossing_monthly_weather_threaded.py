import concurrent.futures
import logging
import os
import threading
import time
from itertools import repeat

import pandas as pd
import requests
from dotenv import load_dotenv
from stairway.apis.visualcrossing.monthly_weather import (
    get_visualcrossing_monthly_weather,
    await_completion,
)

load_dotenv()
thread_local = threading.local()
csv_output_lock = threading.Lock()

logging.basicConfig(level=logging.INFO)

VISUALCROSSING_KEY = os.getenv("VISUALCROSSING_KEY")
URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/historysummary"
# Take into account Visual Crossing API maximum of 10 places in one call
MAX_WORKERS = 2
STEP_SIZE = 10
SLEEP_SECONDS = 5


def main(*args):
    options = parse_args(*args)

    # Read and prep input df
    df_places = (
        pd.read_csv(options.input_path)
        .iloc[int(options.start_index) :]  # subset based on starting index
        .assign(
            location=lambda df: df["lat"].round(6).astype(str)
            + ","
            + df["lng"].round(6).astype(str)
        )[["id", "location"]]
    )

    print(f"Number of places to process: {len(df_places)}")

    # split places into smaller groups for multithreading
    locations = create_subsets_of_list(df_places["location"].to_list())
    place_ids = create_subsets_of_list(df_places["id"].to_list())
    indexes = create_subsets_of_list(df_places.index.to_list())
    places = list(zip(indexes, place_ids, locations))

    # execute the multithreading
    download_all_sites(places, options.output_path)

    print("Done!")


def create_subsets_of_list(list_in, n=STEP_SIZE):
    return [list_in[i * n : (i + 1) * n] for i in range((len(list_in) + n - 1) // n)]


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(locations, output_path):
    indexes, stairway_ids, geolocations = locations
    id_lookup_dict = {k: v for k, v in zip(geolocations, stairway_ids)}

    # create a session for each threat
    session = get_session()
    logging.info(
        f"Processing batch {indexes[0]}-{indexes[-1]} in thread: {threading.get_ident()}"
    )

    # actual API call
    try:
        data = get_visualcrossing_monthly_weather(
            "|".join(geolocations), session, VISUALCROSSING_KEY
        ).json()

        # if locations data is not readily available, query again
        if "locations" not in data:
            # if error, keep retrying until there is a successful response
            while data["errorCode"] != 0:
                logging.info(
                    f"Retry batch {indexes[0]}-{indexes[-1]} in thread: {threading.get_ident()}."
                    + f"Response: {data}."
                )
                time.sleep(SLEEP_SECONDS)
                data = get_visualcrossing_monthly_weather(
                    "|".join(geolocations), session, VISUALCROSSING_KEY
                ).json()
            # now that we have a successful response, await status 'completed'
            logging.info(
                f"Awaiting batch {indexes[0]}-{indexes[-1]} in thread: {threading.get_ident()}"
            )
            data = await_completion(
                data,
                session,
                api_key=VISUALCROSSING_KEY,
                seconds_between_retries=SLEEP_SECONDS,
            )
    except:
        logging.exception(
            logging.warning(
                f"Thread {threading.get_ident()} failed for batch {indexes[0]}-{indexes[-1]}"
                + f" with locations: {geolocations} and response: {data}"
            )
        )
        raise

    # filter out places with no data
    data = [place for place in data["locations"] if place["values"] is not None]
    # add stairway id to each place
    for place in data:
        place.update({"stairway_id": id_lookup_dict[place["name"]]})
    # unnest data
    df_weather = pd.json_normalize(data, "values", ["name", "tz", "stairway_id"])
    logging.info(
        f"Writing batch {indexes[0]}-{indexes[-1]} in thread: {threading.get_ident()}."
        + f"Number of records: {len(df_weather)}"
    )

    # if file does not exist write with header, else append
    with csv_output_lock:
        if not os.path.isfile(output_path):
            df_weather.to_csv(output_path, index=False)
        else:
            df_weather.to_csv(output_path, mode="a", header=False, index=False)


def download_all_sites(sites, output_path):
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_site, sites, repeat(output_path))


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
        default="data/visualcrossing/visualcrossing_monthly_weather_threaded.csv",
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


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
