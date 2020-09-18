import os
import time

import pandas as pd
from dotenv import load_dotenv
from stairway.apis.flickr.photos import (
    get_flickr_images,
    create_image_url,
    create_attribution_url,
)

load_dotenv()


FLICKR_KEY = os.getenv("FLICKR_KEY")
TOP_X_IMAGES = 20
STEP_SIZE = 700


def main(*args):
    options = parse_args(*args)

    # Read and prep input df
    df = (
        pd.read_csv(options.input_path)
        .rename(columns={"id": "stairway_id"})
        .set_index("stairway_id", drop=False)[
            ["stairway_id", "name", "country", "nr_tokens", "wiki_id"]
        ]
    )

    # Process chuncked up input df with a sleep timer of an hour
    for i in range(0, len(df), STEP_SIZE):
        print(f"Now doing places: {i}-{i + STEP_SIZE}")
        df_chunck = df.iloc[i : i + STEP_SIZE]
        df_chunck = process_chunck(df_chunck)

        # if file does not exist write with header, else append
        if not os.path.isfile(options.output_path):
            df_chunck.to_csv(options.output_path, index=False)
        else:
            df_chunck.to_csv(options.output_path, mode="a", header=False, index=False)
        print(f"Done processing places: {i}-{i + STEP_SIZE}")
        print("Sleeping ... zzz")
        time.sleep(60 * 60)


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
        default="data/flickr/flickr_image_list.csv",
        help="Path to the output file.",
    )
    # parser.add_argument(
    #     "-x",
    #     "--top-x-images",
    #     dest="top_x_images",
    #     default=TOP_X_IMAGES,
    #     help="Number of images to retrieve per place.",
    # )

    return parser.parse_args(args=args)


def process_chunck(df):
    return (
        df.reset_index(drop=True)
        .assign(search_string=lambda df: df["name"] + " " + df["country"])
        .groupby("stairway_id")
        .apply(find_flickr_images)
        .reset_index(drop=True)
    )


def find_flickr_images(df, nr_images=TOP_X_IMAGES):
    "Takes a df of a single row and explodes it into the nr of entries found"
    flickr_json = get_flickr_images(
        df["search_string"].iloc[0], api_key=FLICKR_KEY, images_per_page=nr_images
    )["photo"]

    if len(flickr_json) > 0:
        flickr_df = (
            pd.DataFrame(flickr_json)
            .assign(url_b=lambda df: create_image_url(df))
            .assign(image_url=lambda df: create_attribution_url(df))
            #         [['id', 'owner', 'title', 'image_url', 'ownername', 'url_b', 'url_o', 'height_o', 'width_o']]
        )

        repeated_df = pd.concat(
            [df] * len(flickr_json), ignore_index=True
        ).reset_index()[
            ["stairway_id", "index", "name", "country", "nr_tokens", "wiki_id"]
        ]

        df_out = pd.concat([repeated_df, flickr_df], axis=1)
    else:
        df_out = None
    return df_out


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
