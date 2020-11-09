from flask_restful import Resource, reqparse
from resources.utils.distance import sort_places_by_distance

parser = reqparse.RequestParser()
parser.add_argument("n_results", type=int, default=12)
parser.add_argument("seed", type=int, default=1234)


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
                .pipe(sort_places_by_distance, place_id)
                # first get 30 closest places
                .head(30)
                # Sort using the number of tokens weight
                .sample(frac=1, random_state=args["seed"], weights="weight")
                # return the requested subset
                .head(args['n_results'])
                .to_dict(orient="records")
            )
        # if place_id does not exist return nothing
        else:
            places = []

        return {
            "destinations": places,
        }
