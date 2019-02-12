# Cloud Functions

When deploying GCF you literally need to state the name of the function that needs to be executed. 
These functions receive a `flask.Request` object as the sole argument. All routing logic needs to be nested inside that 
function. 
> I am thus unsure whether you can use Flask Resources classes. 

### TODO

- [ ] Discover whether Flask Resource classes can be used in GCF?
    - [ ] If not, rewrite `main.py` into just a function that accepts a `flask.Request` object
    - [ ] Does this mean we need to create a separate function for each request method (GET, POST, DELETE, ...)? 
        - [ ] If so, might be cumbersome to use this method?
- [ ] Think about how/where the db connection string is passed through the function
- [ ] Do we neeed functions for storing the user interactions?
- [ ] Write tests

### uploading to Cloud functions


```bash
(env) $ gcloud beta functions deploy name_of_function --runtime python37 --trigger-http
```


### Tutorials

- https://cloud.google.com/functions/docs/tutorials/http#functions-update-install-gcloud-python
- Good tutorial on setting up cloud functions with Firebase, incl. local testing: https://medium.com/@hiranya911/firebase-using-the-python-admin-sdk-on-google-cloud-functions-590f50226286
- Python cloud function example: https://medium.com/google-cloud/deploying-a-python-serverless-function-in-minutes-with-gcp-19dd07e19824
- tutorial on how to use cloud functions for **React** apps (including use of the Emulator): 
https://www.oreilly.com/learning/serverless-on-google-with-cloud-functions-and-react
    