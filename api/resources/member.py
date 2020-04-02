import pandas as pd
from json import load, dumps
from requests import post
from flask_restful import Resource, reqparse
from resources.utils.utils import create_list_of_likes

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('likes', type=int, required=True, action='append')


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
                   }}
        headers = {'content-type': "application/json"}

        # Use auth for Basic authentication
        r = post('https://us3.api.mailchimp.com/3.0/lists/{}/members/{}/events'.format(self.key['audience_id'],
                                                                                       args['email']),
                 json=payload, headers=headers, auth=('randomstring', self.key['api_key']))

        return r.status_code
