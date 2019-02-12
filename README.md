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
- [ ] Create user interaction database (3 fields: user_id + dest_id + time + action)
- [ ] Create API / Cloud Functions for interacting with a destination.
    - [ ] Adapt random function such that it won't show destinations twice
- [ ] Write tests for Flask APIs / Cloud Functions
- [ ] Build a front-end application
- [ ] Get a "Good" destinations data set


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
