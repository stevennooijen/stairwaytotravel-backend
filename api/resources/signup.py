import pandas as pd
from json import load
from requests import post, get, patch
from flask_restful import Resource, reqparse
from resources.utils.utils import create_list_of_likes

# TODO split into 2 separate parsers, one for query and one for payload/body
# Reason is that you cant set location argument required to True for GET requests
parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('status', type=str, required=False)
parser.add_argument('location', type=str, required=False)
parser.add_argument('likes', type=int, required=False, action='append')


class Signup(Resource):
    def __init__(self, **kwargs):
        with open(kwargs['mailchimp-key'], 'r') as f:
            self.key = load(f)
        self.df = (
            pd.read_csv('./data/wikivoyage_destinations.csv')
        )

    def post(self):
        args = parser.parse_args()
        if args['likes']:
            util_html = create_list_of_likes(self.df, args['likes'])
        else:
            util_html = ''

        payload = {'email_address': args['email'],
                   'status': args['status'],
                   'merge_fields': {
                       "SIGNUP": args['location'],
                       "UTIL_HTML": util_html,
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

        if args['status']:
            payload = {
                "status": args['status']
            }
        elif args['likes']:
            payload = {
                "merge_fields": {'UTIL_HTML': create_list_of_likes(self.df, args['likes'])}
            }
        # hacky code. Should return error if one of these arguments is not provided
        else:
            payload = None

        headers = {'content-type': "application/json"}
        # Use auth for Basic authentication
        r = patch('https://us3.api.mailchimp.com/3.0/lists/{}/members/{}'.format(self.key['audience_id'],
                                                                                 args['email']),
                  json=payload, headers=headers, auth=('randomstring', self.key['api_key']))

        # always succesfull given valid status input, so return doesn't matter
        return r.status_code
