from flask_restful import Resource, reqparse
from resources.utils.features import select_features_with_profiles

parser = reqparse.RequestParser()
parser.add_argument("profiles", type=str, action="append", default=[])


class Destination(Resource):
    def __init__(self, **kwargs):
        # TODO: avoid converting type to object to make it JSON serializable
        self.df = kwargs["df"].astype("object")
        self.df_features = kwargs["df_features"]
        self.df_feature_types = kwargs["df_feature_types"]

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
