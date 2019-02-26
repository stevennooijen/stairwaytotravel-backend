# App Engine

App Engine (AE) basically hosts a Flask application.

### TODO

- [x] Move the db connection string out of the resource class in `destination.py`.
- [ ] Create a Resource for user interactions API?
- [ ] Write tests

### About Flask

The app is split up into three main parts: the routes, the resources, and any common infrastructure.

Then run Flask in `api/` folder:

```bash
python app.py
```

And call the API with:

```bash
# to get a random destination
curl http://127.0.0.1:5000/api/
```
```bash
# to request a specific destination
curl http://127.0.0.1:5000/api/2
```

Flask docs:
- Setting up a simple Flask server: https://flask-restful.readthedocs.io/en/0.3.5/quickstart.html


### About App Engine

- https://cloud.google.com/appengine/docs/standard/python3/
- https://medium.com/google-cloud/deploying-api-via-google-app-engine-1f0209ba5a5e
- https://medium.com/google-cloud/firebase-developing-an-app-engine-service-with-python-and-cloud-firestore-1640f92e14f4


    