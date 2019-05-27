import random

from flask_restful import Resource, reqparse
from google.cloud import firestore

parser = reqparse.RequestParser()
parser.add_argument('continent', type=str)


class Explore(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.key = kwargs['firestore-key']
        self.db = firestore.Client.from_service_account_json(self.key)

    def get(self):
        args = parser.parse_args()

        # if continent provided
        if args['continent']:
            query = (
                self.db
                .collection("destinations-old")
                .where(args['continent'], '==', 1)  # apply continent filter
                .limit(5)
                .get()
            )
        # if no continent argument provided
        else:
            # if no dest_id in url, then set random
            query = (
                self.db
                # TODO: add some randomizer
                .collection("destinations-old")
                .limit(5)
                .get()
            )

        result = {
            "Destinations": [doc.to_dict() for doc in list(query)]
        }

        return result
