import pandas as pd

from flask_restful import Resource, reqparse
from resources.utils.features import select_features_with_profiles

parser = reqparse.RequestParser()
parser.add_argument("profiles", type=str, action="append", default=[])


class Destination(Resource):
    def __init__(self, **kwargs):
        self.df = (
            pd.read_csv("./data/wikivoyage_destinations.csv").set_index(
                "id", drop=False
            )
            # need to do this to convert numpy int and float to native data types
            .astype("object")
        )
        self.df_features = pd.read_csv("./data/wikivoyage_features.csv").set_index("id")
        self.df_feature_types = pd.read_csv("./data/wikivoyage_features_types.csv")

    def get(self, dest_id=None):
        args = parser.parse_args()

        # if dest_id in url, fetch that destination
        if dest_id:
            try:
                doc = self.df.loc[int(dest_id)].to_dict()
            # return null when id not found, or a non-integer id was provided
            except (KeyError, ValueError) as e:
                doc = None

        # if no dest_id in url, fetch random
        else:
            doc = self.df.sample(1).iloc[0].to_dict()

        # add top X features
        doc["features"] = select_features_with_profiles(
            doc["id"], args["profiles"], self.df_features, self.df_feature_types
        )

        return doc
