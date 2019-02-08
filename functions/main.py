from flask import Flask
from flask_restful import Resource, Api

from google.cloud import firestore


app = Flask(__name__)
api = Api(app)

db = firestore.Client.from_service_account_json("../credentials/stairway-firestore-key.json")


class HelloWorld(Resource):
    def get(self):
        # read data
        doc_ref = db.collection('destinations-old').document('1450')
        doc = doc_ref.get()
        doc.to_dict()

        return {doc.id : doc.to_dict()}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
