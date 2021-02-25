# TODO: import logic from notebook `preprocessing-wikivoyage-metadata.ipynb`.


def scope_minimal_nr_tokens(df_in, min_nr_tokens=1):
    """
    Remove destinations with fewer tokens than the set minimum (default: at least 1).
    """
    return df_in.loc[lambda df: df["nr_tokens"] >= min_nr_tokens]
