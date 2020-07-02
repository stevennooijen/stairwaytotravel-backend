import random

import pandas as pd
from stairway.wikivoyage.preprocessing import scope_minimal_nr_tokens
from stairway.utils.utils import add_normalized_column


API_COLUMNS = [
    "id",
    "wiki_id",
    "name",
    "status",
    "type",
    "lat",
    "lng",
    "country",
    "weight",
    "nr_tokens_norm",
]


def main(*args):
    options = parse_args(*args)
    df = (
        pd.read_csv(options.input_path)
        # TODO: remove the rename to the preprocessing piepeline
        .rename(columns={"id": "wiki_id"})
        # TODO: remove the scoping to the preprocessing pipeline
        .pipe(scope_minimal_nr_tokens)
        # add features
        .pipe(add_random_id)
        .pipe(add_sample_weight)
        .pipe(add_normalized_column, "nr_tokens")
    )
    df.to_csv(options.output_path, index=False)
    df.pipe(prepare_for_api).to_csv(options.api_path, index=False)


def parse_args(*args):
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Create features for Wikivoyage data.")
    parser.add_argument(
        "-i",
        "--input-path",
        dest="input_path",
        default="data/wikivoyage/processed/wikivoyage_destinations.csv",
        help="Path to the input file.",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        default="data/wikivoyage/enriched/wikivoyage_destinations.csv",
        help="Path to the output file for future reference.",
    )
    parser.add_argument(
        "-a",
        "--api-path",
        dest="api_path",
        default="api/data/wikivoyage_destinations.csv",
        help="Path to the output file for the API.",
    )

    return parser.parse_args(args=args)


def create_id_mapping(nr_of_digits=6, seed=123):
    """
    Creates a DataFrame where the index can be used to look up a random id in the "id" column.

    Parameters
    ----------
    nr_of_digits: int
        Number of digits to use in the random generated ids.
    seed: int
        Random seed to set to always generate the same mapping.

    Returns
    -------
    out: DataFrame
        DataFrame with an "id" column containing the newly generated X digits ids.
    """
    random.seed(seed)
    hash_min = 10 ** (nr_of_digits - 1)
    hash_max = 10 ** nr_of_digits - 1
    return pd.DataFrame(
        {"id": random.sample(range(hash_min, hash_max), hash_max - hash_min)}
    )


def add_random_id(df_in, id_column_to_map="wiki_id"):
    """
    Maps an integer id column to a random unique 6 digit id using a generated mapping table.

    Parameters
    ----------
    df_in: DataFrame
        Input DataFrame with a integer column to map.
    id_column_to_map: string
        Name of the integer id column to apply the mapping to.

    Returns
    -------
    out: DataFrame
        DataFrame with a new "id" column.
    """
    mapping = create_id_mapping()
    return (
        df_in.set_index(id_column_to_map, drop=False)
        .join(mapping)
        .reset_index(drop=True)
    )


def add_sample_weight(df_in, power_factor=1.5):
    """
    Add a column with weights for biased sampling towards places with a higher number of tokens.

    Parameters
    ----------
    df_in: DataFrame
        Input DataFrame with a "nr_tokens" column containing the number of tokens in a destination text.
    power_factor: float
        Value used for inflating the nr_tokens value to get to the desired sampling weight.

    Returns
    -------
    out: DataFrame
        DataFrame with a "weight" column containing the sampling weights.
    """
    return df_in.assign(weight=lambda df: (df["nr_tokens"] ** power_factor).astype(int))


def prepare_for_api(df_in):
    """
    Prepares the data set to be used in the Flask API.

    Parameters
    ----------
    df_in: DataFrame
        Input data containing all features for the API.

    Returns
    -------
    out: DataFrame
        Prepared DataFrame to be used in the API data folder.
    """

    return (
        df_in
        # keep minimal subset of columns
        [API_COLUMNS]
        # set index for fast lookup
        # .set_index("id", drop=False)
        # need to do this to convert numpy int and float to native data types
        .astype("object")
    )


if __name__ == "__main__":
    import sys

    main(*sys.argv[1:])
