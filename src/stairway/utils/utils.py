import numpy as np


def add_normalized_column(df, column_name):
    """
    Normalize a column and add it to the DataFrame.

    Parameters
    ----------
    df: DataFrame
        Input DataFrame containing the column to normalize.
    column_name: string
        Name of the column to normalize.

    Returns
    -------
    out: DataFrame
        DataFrame with a normalized column having postfix "_norm".
    """
    df[f"{column_name}_norm"] = (df[column_name] - df[column_name].min()) / (
        df[column_name].max() - df[column_name].min()
    )
    return df


# vectorized haversine function
def vectorized_haversine(
    lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371
):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = (
        np.sin((lat2 - lat1) / 2.0) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2.0) ** 2
    )

    return earth_radius * 2 * np.arcsin(np.sqrt(a))
