from numpy.random import normal
import pandas as pd

from flask_restful import Resource, reqparse
from google.cloud import firestore

parser = reqparse.RequestParser()
parser.add_argument('continent', type=str)
parser.add_argument('ne_lat', type=float)
parser.add_argument('ne_lng', type=float)
parser.add_argument('sw_lat', type=float)
parser.add_argument('sw_lng', type=float)

# parameters for osp_importance fitted normal distribution
osp_importance_mu = 0.547
osp_importance_std = 0.144


class Explore(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.key = kwargs['firestore-key']
        self.db = firestore.Client.from_service_account_json(self.key)
        self.db_collection = kwargs['db-collection']
        self.df = pd.read_csv('./data/wikivoyage_destinations.csv')

    def get(self):
        args = parser.parse_args()

        # if continent provided
        if args['continent']:
            query = (
                self.db
                .collection(self.db_collection)
                .where(args['continent'], '==', 1)  # apply continent filter
                # use osp_importance as randomizer
                .where('osp_importance', '<=', normal(osp_importance_mu, osp_importance_std))
                .order_by('osp_importance', direction=firestore.Query.DESCENDING)
                .limit(10)
                .get()
            )
        # if geocoordinates provided (uses Pandas!)
        elif args['ne_lat'] and args['ne_lng'] and args['sw_lat'] and args['sw_lng']:
            subset = (
                self.df
                .loc[lambda df: (df['lat'] >= args['sw_lat']) & (df['lat'] < args['ne_lat'])]
                .loc[lambda df: (df['lng'] >= args['sw_lng']) & (df['lng'] < args['ne_lng'])]
                .sample(10)
                .rename(columns={'pageid': 'id', 'title': 'name', 'country': 'country_name',
                                 'articletype': 'dest_wiki_type', 'lat': 'latitude', 'lng': 'longitude'})
            )
            return {"Destinations": subset.to_dict(orient='records')}

        # if no arguments provided
        else:
            # if no dest_id in url, then set random
            query = (
                self.db
                .collection(self.db_collection)
                # use osp_importance as randomizer
                .where('osp_importance', '<=', normal(osp_importance_mu, osp_importance_std))
                .order_by('osp_importance', direction=firestore.Query.DESCENDING)
                .limit(10)
                .get()
            )

        result = {
            "Destinations": [doc.to_dict() for doc in list(query)]
        }

        return result
