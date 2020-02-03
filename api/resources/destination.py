import pandas as pd

from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()

class Destination(Resource):
    def __init__(self, **kwargs):
        self.df = (
            pd.read_csv('./data/wikivoyage_destinations.csv')
            .rename(columns={'pageid': 'id', 'title': 'name', 'country': 'country_name',
                             'articletype': 'dest_wiki_type', 'lat': 'latitude', 'lng': 'longitude'})
            .set_index('id', drop=False)
            # need to do this to convert numpy int and float to native data types
            .astype('object')
        )

    def get(self, dest_id=None):

        # if dest_id in url, fetch that destination
        if dest_id:
            doc = self.df.loc[int(dest_id)]

        # if no dest_id in url, fetch random
        else:
            doc = self.df.sample(1).iloc[0]

        return doc.to_dict()
