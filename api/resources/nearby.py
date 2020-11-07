from flask_restful import Resource, reqparse
from resources.utils.distance import haversine

parser = reqparse.RequestParser()
parser.add_argument("n_results", type=int, default=12)


class Nearby(Resource):
    def __init__(self, **kwargs):
        self.df = kwargs["df"]

    def get(self, dest_id=None):
        args = parser.parse_args()

        try:
            place_id = int(dest_id)
        except ValueError as e:
            place_id = None

        if place_id in self.df.index:
            places = (
                self.df
                .loc[lambda df: df['id'] != place_id]
                .assign(lat_place=self.df.loc[place_id]['lat'])
                .assign(lng_place=self.df.loc[place_id]['lng'])
                .assign(distance=lambda x: haversine(x['lat'], x['lng'], x['lat_place'], x['lng_place']))
                .sort_values('distance')
                .head(args['n_results'])
                .drop(['distance', 'lat_place', 'lng_place'], axis=1)
                .to_dict(orient="records")
            )
        # if place_id does not exist return nothing
        else:
            places = []

        return {
            "destinations": places,
        }
