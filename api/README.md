# App Engine

App Engine (AE) basically hosts a Flask application.

### TODO

- [x] Move the db connection string out of the resource class in `destination.py`.
- [x] Deploy to Google App Engine
- [x] Solve CORS error for communicating with front-end
- [x] Extend API with argument for searching in a continent
- [x] Create Explore API that returns a list of destinations
- [ ] Create a Resource for user interactions API?
- [ ] Discuss whether there is a 'safer' alternative then deploying `credentials` folder
- [ ] Host on custom domain [`api.stairway.travel`](https://cloud.google.com/appengine/docs/standard/python/mapping-custom-domains)
- [ ] Investigate how to restrict API access
- [ ] Write tests

### About Flask

The app is split up into three main parts: the routes, the resources, and any common infrastructure.

Then run Flask in `api/` folder:

```bash
python main.py
```

And call the API with:

```bash
# to get a random destination
curl http://127.0.0.1:5000/api/

# to request a specific destination: 33 -> Aachen
curl http://127.0.0.1:5000/api/33

# requesting the explore endpoint without arguments, yeilds random places
curl http://127.0.0.1:5000/api/explore/

# requesting with multiple arguments requires quotes
curl "http://127.0.0.1:5000/api/explore/?ne_lat=12.34&ne_lng=5.32&sw_lat=10.1&sw_lng=-3.01"

# see how errors are handled by querying on a small location
curl "http://127.0.0.1:5000/api/explore/?ne_lat=48.9021449&ne_lng=2.4699208&sw_lat=48.815573&sw_lng=2.224199"
curl "http://127.0.0.1:5000/api/explore/?ne_lat=48.8&ne_lng=2.2&sw_lat=48.82&sw_lng=2.22"

# to do a POST request for email signup
curl "http://127.0.0.1:5000/signup/?email=dude@gmail.com&location=/about" -X POST
# or check if the user already exists, do a GET request
curl "http://127.0.0.1:5000/signup/?email=steven.nooijen@hotmail.com" -X GET
# or update a users marketing status with PATCH
url "http://127.0.0.1:5000/signup/?email=steven.nooijen@hotmail.com&status=transactional" -X PATCH

# a POST request for passing liked destinations to a member event
url "http://127.0.0.1:5000/member/?email=steven.nooijen@hotmail.com&likes=461&likes=7787" -X POST 
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

# to request the explore endpoint
curl https://stairway-backend.appspot.com/api/explore/?continent=AF
curl "https://stairway-backend.appspot.com/api/explore/?ne_lat=12.34&ne_lng=5.32&sw_lat=10.1&sw_lng=-3.01"
```

Things to consider:
- Make sure the required dependencies are listed in `requirements.txt`
- Make sure to use the right gcloud configurations
`gcloud config configurations activate stairway`
- Anything in the `api/` folder is uploaded. So this way you can add helper files in for example the `credentials/` 
and `data/` folders. 

To debug, listen to the logs of the deployed app:
```bash
gcloud app logs tail -s default
```


#### Handing secrets to the app deployment

Instead of deploying a `credentials` folder to gcloud, there are two
other ways that might be more secure to handle this:
1. Providing secrets in the [`app.yaml`](https://cloud.google.com/appengine/docs/standard/python/config/appref)
through `env_variables`.
2. Keeping secrets in a [Firestore database](https://stackoverflow.com/questions/22669528/securely-storing-environment-variables-in-gae-with-app-yaml)

#### CORS support

To allow interactions with the Flask resources from different origins
than where Flask is hosted itself (Google App Engine domain), use the
[CORS for Flask](https://flask-cors.readthedocs.io/en/latest/) package.

A list of allowed domains has to be provided in `main.py`:

```python
app = Flask(__name__)
CORS(app, origins=["...", "...", "..."])
```

The front-end is hosted through Google Firebase and creates two domains
for the site: `stairwaytotravel.firebaseapp.com` and
`stairwaytotravel.web.app`. Either one should be added in CORS.

Currently the backend serves both the front-end in production, as well
as the [release branch](`https://stairwaytotravel-release.web.app/`).

#### App Engine resources

- https://cloud.google.com/appengine/docs/standard/python3/
- https://medium.com/google-cloud/deploying-api-via-google-app-engine-1f0209ba5a5e
- https://medium.com/google-cloud/firebase-developing-an-app-engine-service-with-python-and-cloud-firestore-1640f92e14f4
