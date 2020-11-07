import numpy as np
from pandas import DataFrame


def sort_places_by_distance(
    df_places: DataFrame,
    place_id: int,
) -> DataFrame:
    """
    Sort place data on distance from the place provided by 'place_id'.

    Parameters
    ----------
    df_places: DataFrame
        DataFrame containing the places to sort.
    place_id: int
        Id of the place to calculate distances for.

    Returns
    -------
    out: DataFrame
        Place DataFrame sorted by distance to the input place.
    """
    sorted_places = (
        df_places
        .loc[lambda df: df['id'] != place_id]
        .assign(lat_place=df_places.loc[place_id]['lat'])
        .assign(lng_place=df_places.loc[place_id]['lng'])
        .assign(distance=lambda x: haversine(x['lat'], x['lng'], x['lat_place'], x['lng_place']))
        .sort_values('distance')
        .drop(['distance', 'lat_place', 'lng_place'], axis=1)
    )

    return sorted_places


# vectorized haversine function
def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))
