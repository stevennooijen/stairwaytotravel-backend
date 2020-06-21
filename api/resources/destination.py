import pandas as pd

from flask_restful import Resource, reqparse
from resources.utils.selection import select_top_features

parser = reqparse.RequestParser()


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

    def get(self, dest_id=None):

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
        doc["features"] = select_top_features(doc["id"], self.df_features)

        return doc
