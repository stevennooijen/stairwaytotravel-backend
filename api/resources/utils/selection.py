def filter_on_geolocation(df_in, ne_lat, ne_lng, sw_lat, sw_lng):
    return (
        df_in
        .loc[lambda df: (df['lat'] >= sw_lat) & (df['lat'] < ne_lat)]
        .loc[lambda df: (df['lng'] >= sw_lng) & (df['lng'] < ne_lng)]
    )
