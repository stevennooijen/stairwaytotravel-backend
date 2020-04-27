import pandas as pd
from flask_restful import Resource, reqparse
from resources.utils.selection import filter_on_geolocation
from resources.utils.utils import prettify_n_results

parser = reqparse.RequestParser()
parser.add_argument('seed', type=int, default=1234)  # should be required? Otherwise always same results.
parser.add_argument('offset', type=int, default=0)
parser.add_argument('n_results', type=int, default=12)
parser.add_argument('country', type=str)
parser.add_argument('ne_lat', type=float)
parser.add_argument('ne_lng', type=float)
parser.add_argument('sw_lat', type=float)
parser.add_argument('sw_lng', type=float)


class Explore(Resource):
    def __init__(self):
        self.df = (
            pd.read_csv('./data/wikivoyage_destinations.csv')
        )

    def get(self):
        args = parser.parse_args()

        # if no valid arguments, default is to use all places
        subset = self.df

        # if country provided try to match on that first
        country_match = False
        if args['country']:
            subset = self.df.loc[lambda df: df['country'].str.lower() == args['country'].lower()]
            if len(subset) > 0:
                country_match = True
        # if geocoordinates provided and no country match
        if args['ne_lat'] and args['ne_lng'] and args['sw_lat'] and args['sw_lng'] and country_match == False:
            subset = (
                self.df
                .pipe(filter_on_geolocation, args['ne_lat'], args['ne_lng'], args['sw_lat'], args['sw_lng'])
            )

        # select records to output from subset
        try:
            places = (
                subset
                .sample(frac=1, random_state=args['seed'])
                .iloc[args['offset']: args['offset'] + args['n_results']]
            ).to_dict(orient='records')
        # if subset is empty return empty list
        except ValueError:
            places = []

        return {
            "maxPlaces": len(subset),
            "maxPlacesText": prettify_n_results(len(subset)),
            "destinations": places
        }
