import pandas as pd
from json import load
from requests import post, get, patch
from flask_restful import Resource, reqparse
from resources.utils.utils import create_list_of_likes
from resources.utils.interests import create_interests_query

# TODO split into 2 separate parsers, one for query and one for payload/body
# Reason is that you cant set location argument required to True for GET requests
parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True)
parser.add_argument('location', type=str, required=False)
parser.add_argument('status', type=str, required=False)
parser.add_argument('likes', type=int, required=False, action='append')
parser.add_argument('flights', type=bool, required=False, default=False)
parser.add_argument('local_transport', type=bool, required=False, default=False)
parser.add_argument('activities', type=bool, required=False, default=False)
parser.add_argument('accommodation', type=bool, required=False, default=False)
parser.add_argument('none', type=bool, required=False, default=False)


class Signup(Resource):
    def __init__(self, **kwargs):
        with open(kwargs['mailchimp-key'], 'r') as f:
            self.key = load(f)
        self.df = (
            pd.read_csv('./data/wikivoyage_destinations.csv')
        )

    def post(self):
        args = parser.parse_args()

        payload = {'email_address': args['email'],
                   'status': args['status'],
                   'merge_fields': {
                       "SIGNUP": args['location']
                   }}

        # if likes are provided, the booking arguments should also be there
        if args['likes']:
            payload['merge_fields']['UTIL_HTML'] = create_list_of_likes(self.df, args['likes'])
            user_interests = {
                'flights': args['flights'],
                'local_transport': args['local_transport'],
                'activities': args['activities'],
                'accommodation': args['accommodation'],
                'none': args['none'],
            }
            payload['merge_fields']['BOOKING'] = 'Yes' if args['none'] == False else 'No'
            payload['interests'] = create_interests_query(user_interests)

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
