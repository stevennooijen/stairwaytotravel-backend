from numpy.random import normal

from flask_restful import Resource, reqparse
from google.cloud import firestore

parser = reqparse.RequestParser()
parser.add_argument('continent', type=str)

# parameters for osp_importance fitted normal distribution
osp_importance_mu = 0.547
osp_importance_std = 0.144


class Destination(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.key = kwargs['firestore-key']
        self.db = firestore.Client.from_service_account_json(self.key)
        self.db_collection = kwargs['db-collection']

    def get(self, dest_id=None):
        args = parser.parse_args()

        # if dest_id in url, fetch that destination
        if dest_id:
            # read data
            doc_ref = self.db.collection(self.db_collection).document(dest_id)
            doc = doc_ref.get()
            return doc.to_dict()

        # if no dest_id in url, fetch random
        else:
            # if continent provided
            if args['continent']:

                query = (
                    self.db
                    .collection(self.db_collection)
                    .where(args['continent'], '==', 1)  # apply continent filter
                    # use osp_importance as randomizer
                    .where('osp_importance', '<=', normal(osp_importance_mu, osp_importance_std))
                    .order_by('osp_importance', direction=firestore.Query.DESCENDING)
                    .limit(1)
                    .get()
                )
                doc = next(query)
            # if no continent argument provided
            else:
                query = (
                    self.db
                    .collection(self.db_collection)
                    # use osp_importance as randomizer
                    .where('osp_importance', '<=', normal(osp_importance_mu, osp_importance_std))
                    .order_by('osp_importance', direction=firestore.Query.DESCENDING)
                    .limit(1)
                    .get()
                )
                doc = next(query)

            return doc.to_dict()
