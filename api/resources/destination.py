import random

from flask_restful import Resource
from google.cloud import firestore


class Destination(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.key = kwargs['firestore-key']
        self.db = firestore.Client.from_service_account_json(self.key)


    def get(self, dest_id=None):

        # if no dest_id in url, then set random
        if dest_id is None:
            dest_id = str(random.randint(0, 29))

        # read data
        doc_ref = self.db.collection('destinations-old').document(dest_id)
        doc = doc_ref.get()

        return doc.to_dict()
        # return {dest.id : doc.to_dict()}
