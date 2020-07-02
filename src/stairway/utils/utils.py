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
