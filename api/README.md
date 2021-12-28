# Backend API

This README contains a description on the setup of the Flask app, as well as
an instruction on how to deploy the app to Google App Engine (AE).

## 1. About Flask

The app is split up into three main parts: the routes, the resources, and any
common infrastructure. See the
[official documentation](https://flask-restful.readthedocs.io/en/0.3.5/quickstart.html)
for details.

To run Flask locally in the `api/` folder:

```bash
python main.py
```

Then call the API according to the examples below:

```bash
# to get a random destination
curl http://127.0.0.1:5000/api/

# to request a specific destination: 867598 -> Aachen
curl http://127.0.0.1:5000/api/867598

# requesting the explore endpoint without arguments, yeilds random places
curl http://127.0.0.1:5000/api/explore/
curl "http://127.0.0.1:5000/api/explore/?offset=0&n_results=3" -X GET

# requesting with multiple arguments requires quotes
curl "http://127.0.0.1:5000/api/explore/?ne_lat=12.34&ne_lng=5.32&sw_lat=10.1&sw_lng=-3.01"
curl "http://127.0.0.1:5000/api/explore/?offset=0&n_results=3&country=Netherlands" -X GET

# example request with feature profile 'beach'
curl "http://127.0.0.1:5000/api/explore/?seed=40953&n_results=12&offset=0&ne_lat=52.4311573&ne_lng=5.0791619&sw_lat=52.278174&sw_lng=4.7287589&profiles=beach" -X GET

# see how errors are handled by querying on a small location (yields 3 places)
curl "http://127.0.0.1:5000/api/explore/?ne_lat=48.9021449&ne_lng=2.4699208&sw_lat=48.815573&sw_lng=2.224199"
# or a location where nothing is found (yields 0 places)
curl "http://127.0.0.1:5000/api/explore/?ne_lat=48.8&ne_lng=2.2&sw_lat=48.82&sw_lng=2.22"

# Request nearby destinations: 662248 = 's-Hertogenbosch
curl http://127.0.0.1:5000/api/nearby/662248

# to do a POST request for email signup
curl "http://127.0.0.1:5000/signup/?email=dummy@email.com&location=/about&status=subscribed" -X POST
# to do a POST including liked destinations and booking preferences
curl "http://127.0.0.1:5000/signup/?email=dummy@email.com&location=/bucketlist&status=transactional&likes=36&likes=40&likes=33&flights=true&local_transport=true" -X POST
# or check if the user already exists, do a GET request
curl "http://127.0.0.1:5000/signup/?email=dummy@email.com" -X GET
# or update a users marketing status with PATCH
curl "http://127.0.0.1:5000/signup/?email=dummy@email.com&status=subscribed" -X PATCH
# or update liked destinations and booking preferences
curl "http://127.0.0.1:5000/signup/?email=dummy@email.com&likes=7787&likes=461&activities=true" -X PATCH

# a POST request for passing liked destinations to a member event
curl "http://127.0.0.1:5000/member/?email=dummy@email.com&likes=461&likes=7787&none=true" -X POST
```

## 2. About App Engine

Read the basic instructions for a
[standard python environment](https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env).
All you need is:

- `requirements.txt`
- `main.py`
- `app.yaml`

To deploy the app to production run:

```bash
gcloud app deploy --version=production
```

The `--version` flag will make sure to replace an existing instance that shares
that same "version".

With the app running, you can query it as follows:

```bash
# to request a specific destination
curl https://stairway-backend.appspot.com/api/867598

# to request the explore endpoint
curl https://stairway-backend.appspot.com/api/explore/?continent=AF
curl "https://stairway-backend.appspot.com/api/explore/?ne_lat=12.34&ne_lng=5.32&sw_lat=10.1&sw_lng=-3.01"
```

Things to consider:
- Make sure the required dependencies are listed in `requirements.txt`.
- Make sure to use the right gcloud configurations
`gcloud config configurations activate`.
- Anything in the `api/` folder is uploaded. So this way you can add helper
files in for example `credentials/` and `data/` folders.

### Debugging

To debug, listen to the logs of the deployed app:

```bash
gcloud app logs tail -s default
```

Additionally, there's a small script named `profile-flask.py` that can be run
to profile the web application and find factors that negatively influence the
app's performance.

### CORS support

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
