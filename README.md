# README

Set up simple backend web-service with GCP.

## What do I want to do?

Eventually:
- Database with destinations 
    - GET destinations
- Database for user interaction
    - POST interactions (like, dislike, view, click)
    - GET liked destinations
- Login to save userid and retrieve liked destinations

Requirements:
- Create 2 databases
- Create API requests
    - Either cloud functions; OR
    - App engine services

ToDo checklist: 
- [x] Create destinations database
- [ ] Create Cloud Function for retrieving (random) destinations from the DB
    - [x] Set up local Flask to test the API / emulate the function
- [ ] Create API / Cloud Functions for interacting with a destination.
    - [ ] Adapt random function such that it won't show destinations twice
- [ ] Create user interaction database (3 fields: user_id + dest_id + time + action)
- [ ] Write tests for Flask APIs / Cloud Functions
- [x] Build a front-end application
- [ ] Get a "Good" destinations data set
    - [x] For current Stairway set, use destinations with `succes > 0`
    - [ ] Make sure all destinations are succesfully parsed
    - [ ] Save continent in one variable, instead of one for each continent
    - [ ] Add array with all parents. Then use `array_contains` filter
    to select all destinations that are within a certain `parent` region
    - [ ] For activity labels possibly use Spacy and Prodigy
- [ ] Set good (composite?) indices on Firestorm
    - [x] One for each `continent` + `osp_importance`

## Functionality

3 APIs needed:
1. Request a list of recommendations to explore
2. Request a specific destination to read more about it
3. Request a list of liked destinations for the bucketlist

API 1: Exploring:
1. User gets an initial list of destinations
    - API returns **random** destinations
2. User likes/dislikes a couple of them
    - likes/dislikes are maintained in React `sessionStorage`
3. User gets a new/updates list of destinations
    - API has likes/dislikes as additional parameter
    - Back-end model uses likes/dislikes to get new destinations
4. Step 2 and 3 keep repeating

API 2: Getting to know:
1. User clicks on 'Read more' to retrieve specific destination page
    - API returns that destination
2. User can like/dislike
3. And will then have to return to Exploring or go to a different tab.

API 3: Retrieving wishlist
1. User goes to bucketlist tab
    - API returns liked destinations


## Recommendations

Old Stairway implementation is through BM25 and works as follows:
1. The activity query from the user is a list with binary values for the
activity types that the user wants to search on. See
[`Profile.load_query()`](https://github.com/Braamling/project_travel/blob/432b21d7df96de3e456541d893d1f7a03a631836/REST_API/project_travel/classes/profile.py)
2. This columns list is then used as input for
[`bm25.recommend()`](https://github.com/Braamling/project_travel/blob/432b21d7df96de3e456541d893d1f7a03a631836/REST_API/project_travel/controllers/recommend.py)
3. Which on its turn does an inner join between the `destinations` and
`destination_scores` table to retrieve and return the destinations that
score best. Scoring is done by summing the scores of each activity in
the query over the destination.
See [`BM25Recommendations.query()`](https://github.com/Braamling/project_travel/blob/432b21d7df96de3e456541d893d1f7a03a631836/REST_API/project_travel/dao/bm25Recommendations.py)

To incorporate this, investigate:
- to what extend activity scores from `destination_scores` should be
included in Firestore.
    - Likely hard to do, as we need to score ALL destinations and
    Firestore is not meant for querying everything. Better to fetch the
    resulting destination ids from the calculations and retrieve those
    individually from Firestore.
    - Alternatively, use Firestorm's `array_contains` filter. However
    doesn't allow sorting on relevancy. It either contains the activity
    or not (boolean), so you loose some sensitivity
- if not possible, whether to read in these scores from for example a
storage bucket and keep the scores in memory while processing.
    - Logic for summing activity scores based on query is done in python
    and this API should return a list of destinations ids that can then
    be used for retrieval in Firestore.
    - this means however that other filters like continent, budget and
    temperature should also be taken into account in python before
    retrieving the destination ids...?


## Installing package

For development, install the `stairway` package in the virtual
environment with:

```bash
pip install --editable .
```

## Components

### Two serverless options for hosting:

1. Cloud Functions
    - Define functions that accept a `flask.Request` object and deploy that. 
    - Although some tips & tricks, best practices and tests in the documentation, a Python emulator is not existent. 

2. App Engine
    - Create local Flask App then deploy on GCP.
    - Your apps scale automatically to meet traffic demand.    

[Difference](https://www.quora.com/Whats-the-difference-between-Cloud-Functions-and-App-Engine-in-Google-Cloud): 
Cloud Functions is a straightforward “serverless” offering, while App Engine can be used to customize 
the application infrastructure that meets the needs of your app. In other words: App Engine is more flexible.

### Database to be used:

Cloud Firestore is THE database to be used:
- Flexible, scalable NoSQL cloud database to store and sync data for client- and server-side development.
- Has Admin SDK for python to read and write from Firestore
- (Cloud Firestore is the next major version of Cloud Datastore and a re- branding of the product.)
- (Firebase Realtime Database is just a giant JSON tree, Cloud Firestore is a little more structured and flexible.)

Both Cloud Functions and App Engine can connect to the database.

See `notebooks/` folder for reference material on how to use Firestore.

NOTE: the [free tier](https://firebase.google.com/docs/firestore/quotas) allows 20.000 writes/deletes per day and up to 
1GB of data. Number of free reads per day is 50.000. So take care to stay below that! This might become an issue when 
we want to do more advanced modelling that needs to read/score the entire data set. Also it might be troublesome quickly 
in case the number of users picks up. For now, just go with it!

 

### Combining both:

Firebase & App Engine:
- Lijkt bingo! https://medium.com/google-cloud/firebase-developing-an-app-engine-service-with-python-and-cloud-firestore-1640f92e14f4

Firebase & Functions:
- Using Java, but looks good: https://rominirani.com/build-a-serverless-online-quiz-with-google-cloud-functions-and-cloud-firestore-1e3fbf84a7d8



## When developing:

Set right credentials:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credentials/stairway-firestore-key.json"
```

Or explicitly reference service account credentials when executing code.
