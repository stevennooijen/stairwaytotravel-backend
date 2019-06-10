from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources.destination import Destination
from resources.explore import Explore

app = Flask(__name__)
CORS(app, origins=["https://stairwaytotravel.firebaseapp.com", "https://stairway.travel", "http://localhost:3000"])
api = Api(app)

FIRESTORE_KEY = 'credentials/stairway-firestore-key.json'
db_collection = 'destinations'

api.add_resource(Destination, '/api/',
                 resource_class_kwargs={'firestore-key': FIRESTORE_KEY, 'db-collection': db_collection})
api.add_resource(Destination, '/api/<dest_id>', endpoint='dest_ep',
                 resource_class_kwargs={'firestore-key': FIRESTORE_KEY, 'db-collection': db_collection})
api.add_resource(Explore, '/api/explore/',
                 resource_class_kwargs={'firestore-key': FIRESTORE_KEY, 'db-collection': db_collection})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
