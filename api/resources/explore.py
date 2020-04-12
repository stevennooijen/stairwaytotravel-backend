import pandas as pd

from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('seed', type=int, default=1234)  # should be required? Otherwise always same results.
parser.add_argument('offset', type=int, default=0)
parser.add_argument('n_results', type=int, default=10)
parser.add_argument('ne_lat', type=float)
parser.add_argument('ne_lng', type=float)
parser.add_argument('sw_lat', type=float)
parser.add_argument('sw_lng', type=float)

def filter_on_geolocation(df_in, ne_lat, ne_lng, sw_lat, sw_lng):
    return (
        df_in
        .loc[lambda df: (df['lat'] >= sw_lat) & (df['lat'] < ne_lat)]
        .loc[lambda df: (df['lng'] >= sw_lng) & (df['lng'] < ne_lng)]
    )


class Explore(Resource):
    def __init__(self):
        self.df = (
            pd.read_csv('./data/wikivoyage_destinations.csv')
        )

    def get(self):
        args = parser.parse_args()

        # if geocoordinates provided (uses Pandas!)
        if args['ne_lat'] and args['ne_lng'] and args['sw_lat'] and args['sw_lng']:
            try:
                subset = (
                    self.df
                    .pipe(filter_on_geolocation, args['ne_lat'], args['ne_lng'], args['sw_lat'], args['sw_lng'])
                    .sample(frac=1, random_state=args['seed'])
                    .iloc[args['offset'] : args['offset'] + args['n_results']]
                ).to_dict(orient='records')
            except ValueError:
                subset = []

        # if no arguments provided
        else:
            # if no dest_id in url, then set random
            subset = (
                self.df
                .sample(frac=1, random_state=args['seed'])
                # .head(N_RESULTS)
                .iloc[args['offset']: args['offset'] + args['n_results']]
            ).to_dict(orient='records')

        return {"Destinations": subset}
