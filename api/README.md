# App Engine

App Engine (AE) basically hosts a Flask application.

### TODO

- [x] Move the db connection string out of the resource class in `destination.py`.
- [x] Deploy to Google App Engine
- [ ] Create a Resource for user interactions API?
- [ ] Discuss whether there is a 'safer' alternative then deploying `credentials` folder
- [ ] Investigate how to restrict API access
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

Basic instructions [here](https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env)

All you need is:
- requirements.txt
- main.py
- app.yaml

Then just do:

```bash
gcloud app deploy

# to request a specific destination
curl https://stairway-backend.appspot.com/api/2
```

Things to consider:
- Make sure the required dependencies are listed in `requirements.txt`


#### Handing secrets to the app deployment

Instead of deploying a `credentials` folder to gcloud, there are two
other ways that might be more secure to handle this:
1. Providing secrets in the [`app.yaml`](https://cloud.google.com/appengine/docs/standard/python/config/appref)
through `env_variables`.
2. Keeping secrets in a [Firestore database](https://stackoverflow.com/questions/22669528/securely-storing-environment-variables-in-gae-with-app-yaml)

#### App Engine resources

- https://cloud.google.com/appengine/docs/standard/python3/
- https://medium.com/google-cloud/deploying-api-via-google-app-engine-1f0209ba5a5e
- https://medium.com/google-cloud/firebase-developing-an-app-engine-service-with-python-and-cloud-firestore-1640f92e14f4


    