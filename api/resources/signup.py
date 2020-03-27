from json import load
from requests import post, get, patch
from flask_restful import Resource, reqparse

# TODO split into 2 separate parsers, one for query and one for payload/body
# Reason is that you cant set location argument required to True for GET requests
parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('status', type=str, default='subscribed', required=False)
parser.add_argument('location', type=str, required=False)


class Signup(Resource):
    def __init__(self, **kwargs):
        with open(kwargs['mailchimp-key'], 'r') as f:
            self.key = load(f)

    def post(self):
        args = parser.parse_args()

        payload = {'email_address': args['email'],
                   'status': args['status'],
                   'merge_fields': {
                       "SIGNUP": args['location']
                   }}
        headers = {'content-type': "application/json"}

        # Use auth for Basic authentication
        r = post('https://us3.api.mailchimp.com/3.0/lists/{}/members/'.format(self.key['audience_id']),
                 json=payload, headers=headers, auth=('randomstring', self.key['api_key']))

        try:
            member_id = r.json()['id']
        except KeyError:
            member_id = None

        return member_id

    def get(self):
        args = parser.parse_args()

        r = get('https://us3.api.mailchimp.com/3.0/lists/{}/members/{}'.format(self.key['audience_id'], args['email']),
                auth=('randomstring', self.key['api_key']))

        try:
            member_id = r.json()['id']
        except KeyError:
            member_id = None

        return member_id

    def patch(self):
        args = parser.parse_args()

        payload = {
            "status": args['status']
        }
        headers = {'content-type': "application/json"}

        # Use auth for Basic authentication
        r = patch('https://us3.api.mailchimp.com/3.0/lists/{}/members/{}'.format(self.key['audience_id'],
                                                                                 args['email']),
                  json=payload, headers=headers, auth=('randomstring', self.key['api_key']))

        # always succesfull given valid status input, so return doesn't matter
        return r.status_code
