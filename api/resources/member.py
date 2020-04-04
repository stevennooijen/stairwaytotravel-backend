import pandas as pd
from json import load, dumps
from requests import post
from flask_restful import Resource, reqparse
from resources.utils.utils import create_list_of_likes

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('likes', type=int, required=True, action='append')
parser.add_argument('flights', type=bool, required=False, default=False)
parser.add_argument('local_transport', type=bool, required=False, default=False)
parser.add_argument('activities', type=bool, required=False, default=False)
parser.add_argument('accommodation', type=bool, required=False, default=False)
parser.add_argument('none', type=bool, required=False, default=False)

class Member(Resource):
    def __init__(self, **kwargs):
        with open(kwargs['mailchimp-key'], 'r') as f:
            self.key = load(f)
        self.df = (
            pd.read_csv('./data/wikivoyage_destinations.csv')
        )

    def post(self):
        args = parser.parse_args()

        likes_text = create_list_of_likes(self.df, args['likes'],
                                          list_prefix='|', list_postfix='', line_prefix=' ', line_postfix=' |')

        payload = {"name": "liked_destinations",
                   "properties": {
                       "likes_ids": dumps(args['likes']),
                       "likes_titles": dumps(likes_text),
                       'book_flights': 'Yes' if args['flights'] == True else 'No',
                       'book_local_transport': 'Yes' if args['local_transport'] == True else 'No',
                       'book_activities': 'Yes' if args['activities'] == True else 'No',
                       'book_accommodation': 'Yes' if args['accommodation'] == True else 'No',
                       'book_nothing': 'Yes' if args['none'] == True else 'No',
                   }}
        print(payload)
        headers = {'content-type': "application/json"}

        # Use auth for Basic authentication
        r = post('https://us3.api.mailchimp.com/3.0/lists/{}/members/{}/events'.format(self.key['audience_id'],
                                                                                       args['email']),
                 json=payload, headers=headers, auth=('randomstring', self.key['api_key']))

        return r.status_code
