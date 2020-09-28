import logging
import time

import pandas as pd
from PIL import UnidentifiedImageError
from stairway.instagram.image import create_instagram_image

TOP_X_IMAGES = 5
STEP_SIZE = 1000
SLEEP_SECONDS = 60 * 5


def main(*args):
    options = parse_args(*args)

    # Read and prep input df
    df_images = (
        pd.read_csv(options.input_path)
        .loc[lambda df: df["index"] < TOP_X_IMAGES]
        .assign(
            output_path=lambda df: options.output_path
            + df["stairway_id"].astype(str)
            + "-"
            + df["index"].astype(str)
            + ".jpeg"
        )
    )

    print(f"Number of images to create: {len(df_images)}")

    # Process chuncked up input df with a sleep timer of an hour
    for i in range(int(options.start_index), len(df_images), STEP_SIZE):
        print(f"Now doing images: {i}-{i + STEP_SIZE}")
        df_images.iloc[i : i + STEP_SIZE].apply(process_row, axis=1)

        print(f"Done processing images: {i}-{i + STEP_SIZE}")
        print("Sleeping ... zzz")
        time.sleep(SLEEP_SECONDS)

    print("Done!")


def parse_args(*args):
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Create Instagram images from list of image locations."
    )
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
        default="/Users/terminator/travel/instagram-images/",
        help="Path to the output folder.",
    )
    parser.add_argument(
        "-s",
        "--start-index",
        dest="start_index",
        default=0,
        help="Index of first image to start processing",
    )

    return parser.parse_args(args=args)


def process_row(row):
    try:
        create_instagram_image(
            row["url_b"], row["name"], row["country"], row["output_path"]
        )
    except UnidentifiedImageError:
        logging.warning(
            f"Failed at image {row['stairway_id']}-{row['index']} with url_b: {row['url_b']}"
        )
        try:
            create_instagram_image(
                row["url_o"], row["name"], row["country"], row["output_path"]
            )
        except:
            logging.exception(
                logging.warning(
                    f"Failed at image {row['stairway_id']}-{row['index']} with url_o: {row['url_o']}"
                )
            )
            pass


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
