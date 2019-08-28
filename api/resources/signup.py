from json import load
from requests import post
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('email', type=str)


class Signup(Resource):
    def __init__(self, **kwargs):
        with open(kwargs['mailchimp-key'], 'r') as f:
            self.key = load(f)

    # test connection
    # def get(self):
    #     return get('https://us3.api.mailchimp.com/3.0/').json()

    def post(self):
        args = parser.parse_args()

        payload = {'email_address': args['email'], 'status': 'subscribed'}
        headers = {'content-type': "application/json"}

        # Use auth for Basic authentication
        r = post('https://us3.api.mailchimp.com/3.0/lists/{}/members/'.format(self.key['audience_id']),
                 json=payload, headers=headers, auth=('randomstring', self.key['api_key']))

        return r.status_code
