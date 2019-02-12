import random

from flask_restful import Resource
from google.cloud import firestore


class Destination(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.key = kwargs['firestore-key']
        self.db = firestore.Client.from_service_account_json(self.key)


    def get(self):
        # read data
        doc_id = str(random.randint(0, 29))
        doc_ref = self.db.collection('destinations-old').document(doc_id)
        doc = doc_ref.get()
        doc.to_dict()

        return {doc.id : doc.to_dict()}
