from json import load, dumps
from requests import post
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('likes', type=int, required=True, action='append')


class Member(Resource):
    def __init__(self, **kwargs):
        with open(kwargs['mailchimp-key'], 'r') as f:
            self.key = load(f)

    def post(self):
        args = parser.parse_args()

        payload = {"name": "liked_destinations",
                   "properties": {
                       "likes_ids": dumps(args['likes']),
                   }}
        headers = {'content-type': "application/json"}

        # Use auth for Basic authentication
        r = post('https://us3.api.mailchimp.com/3.0/lists/{}/members/{}/events'.format(self.key['audience_id'],
                                                                                       args['email']),
                 json=payload, headers=headers, auth=('randomstring', self.key['api_key']))

        return r.status_code
