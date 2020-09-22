import logging
import os
import time

import pandas as pd
from stairway.apis.wikivoyage.page_info import get_wikivoyage_page_info


# Be reasonable with querying, always query 50 at once to reduce burden
BATCH_SIZE = 50  # number of queries per batch
PAGES_PER_QUERY = 50
SLEEP_SECONDS = 60 * 5


def main(*args):
    options = parse_args(*args)

    # Read and prep input df
    page_ids = pd.read_csv(options.input_path)["wiki_id"].tolist()

    print(f"Number of pages to process: {len(page_ids)}")

    # Process chuncked up input df with a sleep timer of an hour
    for batch in range(
        options.start_index, len(page_ids), BATCH_SIZE * PAGES_PER_QUERY
    ):
        print(f"Now doing batch: {batch}-{batch + BATCH_SIZE * PAGES_PER_QUERY}")

        df_batch = pd.concat(
            [
                pd.DataFrame.from_dict(
                    get_wikivoyage_page_info(page_ids[query : query + PAGES_PER_QUERY]),
                    orient="index",
                )
                for query in range(
                    batch, batch + BATCH_SIZE * PAGES_PER_QUERY, PAGES_PER_QUERY
                )
            ]
        )

        # if file does not exist write with header, else append
        if not os.path.isfile(options.output_path):
            df_batch.to_csv(options.output_path, index=False)
        else:
            df_batch.to_csv(options.output_path, mode="a", header=False, index=False)
        print(f"Done with batch: {batch}-{batch + BATCH_SIZE * PAGES_PER_QUERY}")
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
        default="data/wikivoyage/enriched/wikivoyage_destinations.csv",
        help="Path to the destinations input file.",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        default="data/wikivoyage/clean/wikivoyage_page_info.csv",
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
