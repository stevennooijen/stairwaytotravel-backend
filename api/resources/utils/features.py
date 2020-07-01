def select_features(place_id, df_features, top_x=5, min_threshold=0.1):
    """
    Get top x most relevant features for a place.

    Parameters
    ----------
    place_id: int
        Place ID to return features for.
    df_features: DataFrame
        Data set with feature scores for all places.
    top_x: int
        Number of features to return in descending order of feature score.
    min_threshold: float
        Minimum score a feature needs to have.

    Returns
    -------
    out: list
        List with the top x feature names.
    """
    return (
        df_features.loc[place_id]
        .loc[lambda x: x > min_threshold]
        .sort_values(ascending=False)[:top_x]
        .index.tolist()
    )


def select_feature_columns_with_profiles(profiles, df_feature_types):
    """
    Return names of features in scope for the provided profiles.

    Parameters
    ----------
    profiles: list
        List with feature profiles in scope (e.g. 'nature', 'culture', ...).
    df_feature_types: DataFrame
        Data set that tells which features belong to which feature profiles.

    Returns
    -------
    out: list
        List with the top x feature names.
    """
    return (
        df_feature_types.set_index("feature_name")[profiles]
        .sum(axis=1)
        .loc[lambda x: x > 0]
        .index.values
    )


def select_features_with_profiles(
    place_id, feature_profiles, df_features, df_feature_types, top_x=5, *kwargs
):
    """
    Get top_x features for a place, keeping feature profiles into account.

    If feature profiles is an empty list, return most relevant features for the place.

    Parameters
    ----------
    place_id: int
        Place ID to return features for.
    feature_profiles: list
        List with feature profiles in scope (e.g. 'nature', 'culture', ...).
    df_features: DataFrame
        Data set with feature scores for all places.
    df_feature_types: DataFrame
        Data set that tells which features belong to which feature profiles.
    top_x: int
        Number of features to return in descending order of feature score.

    Returns
    -------
    out: list
        List with the top x feature names, with features from selected profiles first.
    """
    features_inscope = select_feature_columns_with_profiles(
        feature_profiles, df_feature_types
    )
    df_features_inscope = df_features[features_inscope]

    result = select_features(place_id, df_features_inscope, *kwargs)

    if len(result) < top_x:
        df_features_outscope = df_features.drop(features_inscope, axis=1)
        result += select_features(place_id, df_features_outscope, *kwargs)[
            : (top_x - len(result))
        ]

    return result
