import pandas as pd
from flask_restful import Resource, reqparse
from resources.utils.features import (
    select_features_with_profiles,
    filter_and_sort_places_by_profiles,
)
from resources.utils.selection import filter_on_geolocation
from resources.utils.utils import prettify_n_results

PROFILE_WEIGHT_FACTOR = 1.5
PROFILE_WEIGHT_THRESHOLD = 1
OUTPUT_COLUMNS = [
    "id",
    "wiki_id",
    "name",
    "status",
    "type",
    "lat",
    "lng",
    "country",
    "features",
]

parser = reqparse.RequestParser()
parser.add_argument("seed", type=int, default=1234)
parser.add_argument("offset", type=int, default=0)
parser.add_argument("n_results", type=int, default=12)
parser.add_argument("country", type=str)
parser.add_argument("ne_lat", type=float)
parser.add_argument("ne_lng", type=float)
parser.add_argument("sw_lat", type=float)
parser.add_argument("sw_lng", type=float)
parser.add_argument("profiles", type=str, action="append", default=[])


class Explore(Resource):
    def __init__(self):
        self.df = pd.read_csv("./data/wikivoyage_destinations.csv").set_index(
            "id", drop=False
        )
        self.df_features = pd.read_csv("./data/wikivoyage_features.csv").set_index("id")
        self.df_feature_types = pd.read_csv("./data/wikivoyage_features_types.csv")

    def get(self):
        args = parser.parse_args()

        # if no valid arguments, default is to use all places
        subset = self.df

        # if country provided try to match on that first
        country_match = False
        if args["country"]:
            subset = self.df.loc[
                lambda df: df["country"].str.lower() == args["country"].lower()
            ]
            if len(subset) > 0:
                country_match = True
        # if geocoordinates provided and no country match
        if (
            args["ne_lat"]
            and args["ne_lng"]
            and args["sw_lat"]
            and args["sw_lng"]
            and country_match == False
        ):
            subset = self.df.pipe(
                filter_on_geolocation,
                args["ne_lat"],
                args["ne_lng"],
                args["sw_lat"],
                args["sw_lng"],
            )
        # if feature profiles provided, filter and sort on that
        if args["profiles"]:
            subset = subset.pipe(
                filter_and_sort_places_by_profiles,
                args["profiles"],
                self.df_features,
                self.df_feature_types,
                profile_weight_factor=PROFILE_WEIGHT_FACTOR,
                profile_weight_threshold=PROFILE_WEIGHT_THRESHOLD,
            )
        # if not, sort using the number of tokens weight (if places in subset at all)
        elif len(subset) > 0:
            subset = subset.sample(frac=1, random_state=args["seed"], weights="weight")

        # apply offset if places found
        try:
            places = subset.iloc[
                args["offset"] : args["offset"] + args["n_results"]
            ].copy()
            # add top X features
            places["features"] = places["id"].apply(
                lambda x: select_features_with_profiles(
                    x, args["profiles"], self.df_features, self.df_feature_types
                )
            )
            # select columns and return as dict
            places = places[OUTPUT_COLUMNS].to_dict(orient="records")
        # if subset is empty return empty list
        except ValueError:
            places = []

        return {
            "maxPlaces": len(subset),
            "maxPlacesText": prettify_n_results(len(subset)),
            "destinations": places,
        }
