# README

Set up simple backend web-service with GCP.

## Components

### Two serverless options for hosting:

1. Cloud Functions
    - Literally as simple as defining a function and deploying that. 
    - https://cloud.google.com/functions/docs/tutorials/http#functions-update-install-gcloud-python
    - Good tutorial on how to use cloud functions for React apps (including use of the Emulator): 
    https://www.oreilly.com/learning/serverless-on-google-with-cloud-functions-and-react
    - Python cloud function example: https://medium.com/google-cloud/deploying-a-python-serverless-function-in-minutes-with-gcp-19dd07e19824
    
2. App Engine
    - Create local Flask App then deploy on GCP
    - Your apps scale automatically to meet traffic demand.
    - https://cloud.google.com/appengine/docs/standard/python3/
    - https://medium.com/google-cloud/deploying-api-via-google-app-engine-1f0209ba5a5e
    

Difference: Cloud Functions is a straightforward “serverless” offering, while App Engine can be used to customize 
the application infrastructure that meets the needs of your app. In other words: App Engine is more flexible.
https://www.quora.com/Whats-the-difference-between-Cloud-Functions-and-App-Engine-in-Google-Cloud

### Database to be used:

Cloud Firestore is THE database to be used:
- Flexible, scalable NoSQL cloud database to store and sync data for client- and server-side development.
- Has Admin SDK for python to read and write from Firestore
- Tutorial for getting started with cloud firestore with Python: https://www.youtube.com/watch?v=yylnC3dr_no 
- https://firebase.google.com/docs/firestore/
- https://cloud.google.com/firestore/docs/data-model
- (Cloud Firestore is the next major version of Cloud Datastore and a re- branding of the product.)
- (Firebase Realtime Database is just a giant JSON tree, Cloud Firestore is a little more structured and flexible.)

Both functions and engine can connect to the database.

Setup instructions:
- Follow: https://cloud.google.com/firestore/docs/quickstart-servers
- Create new GCP project
- Create service account for firestore

NOTE: the [free tier](https://firebase.google.com/docs/firestore/quotas) allows 20.000 writes/deletes per day and up to 
1GB of data. Number of free reads per day is 50.000. So take care to stay below that! This might become an issue when 
we want to do more advanced modelling that needs to read/score the entire data set. Also it might be troublesome quickly 
in case the number of users picks up. For now, just go with it!

 

### Combining both:

Firebase & App Engine:
- Lijkt bingo! https://medium.com/google-cloud/firebase-developing-an-app-engine-service-with-python-and-cloud-firestore-1640f92e14f4

Firebase & Functions:
- Using Java, but looks good: https://rominirani.com/build-a-serverless-online-quiz-with-google-cloud-functions-and-cloud-firestore-1e3fbf84a7d8


## What do I want to do?

Eventually:
- Database with destinations 
    - GET destinations
- Database for user interaction
    - POST interactions (like, dislike, view, click)
    - GET liked destinations
- Login to save userid and retrieve liked destinations

At first: 
- Create 2 databases
- Create API requests
    - Either cloud functions; OR
    - App engine services


## When developing:

Set right credentials:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="credentials/stairway-firestore-key.json"
```