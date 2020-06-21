N_FEATURES = 5


def filter_on_geolocation(df_in, ne_lat, ne_lng, sw_lat, sw_lng):
    return df_in.loc[lambda df: (df["lat"] >= sw_lat) & (df["lat"] < ne_lat)].loc[
        lambda df: (df["lng"] >= sw_lng) & (df["lng"] < ne_lng)
    ]


def select_top_features(place_id, df_in, top_x=N_FEATURES):
    """
    Selects top X features with the highes scores and returns them in a list.
    """
    return df_in.loc[place_id].sort_values(ascending=False)[:top_x].index.tolist()
