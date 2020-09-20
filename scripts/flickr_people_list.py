import os
import time

import pandas as pd
from dotenv import load_dotenv
from stairway.apis.flickr.people import get_flickr_people_info, parse_flickr_people_info

load_dotenv()


FLICKR_KEY = os.getenv("FLICKR_KEY")
# Take into account Flickr API usage limit of max 3600 calls an hour
STEP_SIZE = 100
SLEEP_SECONDS = 60 * 10


def main(*args):
    options = parse_args(*args)

    # Read and prep input df
    authors = pd.read_csv(options.input_path)["owner"].drop_duplicates()

    print(f"Number of authors to process: {len(authors)}")

    # Process chuncked up input df with a sleep timer of an hour
    for i in range(0, len(authors), STEP_SIZE):
        print(f"Now doing authors: {i}-{i + STEP_SIZE}")
        authors_chunck = authors.iloc[i : i + STEP_SIZE]
        authors_chunck = process_chunck(authors_chunck)

        # if file does not exist write with header, else append
        if not os.path.isfile(options.output_path):
            authors_chunck.to_csv(options.output_path, index=False)
        else:
            authors_chunck.to_csv(
                options.output_path, mode="a", header=False, index=False
            )
        print(f"Done processing authors: {i}-{i + STEP_SIZE}")
        print("Sleeping ... zzz")
        time.sleep(SLEEP_SECONDS)

    print("Done!")


def parse_args(*args):
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Create list of Flickr images for all places.")
    parser.add_argument(
        "-i",
        "--input-path",
        dest="input_path",
        default="data/flickr/flickr_image_list.csv",
        help="Path to the place images input file.",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        default="data/flickr/flickr_people_list.csv",
        help="Path to the output file.",
    )

    return parser.parse_args(args=args)


def process_chunck(authors):
    return pd.DataFrame(
        [
            parse_flickr_people_info(get_flickr_people_info(author, api_key=FLICKR_KEY))
            for author in authors
        ]
    )[["nsid", "username", "realname", "path_alias", "location", "profileurl"]]


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
