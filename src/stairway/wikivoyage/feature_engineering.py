import random
import pandas as pd


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
        DataFrame with a new "id" column
    """
    mapping = create_id_mapping()
    return (
        df_in.set_index(id_column_to_map, drop=False)
        .join(mapping)
        .reset_index(drop=True)
    )
