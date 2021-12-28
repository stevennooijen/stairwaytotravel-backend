# Stairway to Travel: Backend

This is the code repository containing backend related services for [Stairway
to Travel](https://stairwaytotravel.com/). The repository's focus is on
preparing data and creating a simple backend web-service API on Google Cloud
Platform (GCP).

## Folder structure

    .
    ├── api               # Flask API files for Google App Engine
    ├── data              # Helper folder for local file storage
    ├── documentation     # Diagrams and detailed documentation
    ├── notebooks         # Jupyter notebooks for demos and experimentation
    ├── scripts           # Scripts for ingesting large amounts of data
    ├── src               # Core functionality for preparing data
    ├── tests             # Tets on core functions (but limited - WIP)
    ├── environment.yml   # Requirements for Conda environment
    └── README.md

## Preparing your working environment

First prepare the Conda virtual environment:

```bash
conda env create --file environment.yml
conda activate stairwaytotravel-backend
```

Then install the `stairway` package in the virtual environment in editable
mode so that any changes in your package are directly available in your
notebook when using `%autoreload`.

```bash
pip install --editable .
```

## Credentials

Several scripts and functions require credentials to access third party APIs
like Flickr, Mailchimp or Google App Engine. These keys have not been uploaded
to Git and you will have to get your own keys for access to these tools.

Retrieval of the keys happens in two ways:

1. Either through a `.env` file using the
[`python-dotenv`](https://pypi.org/project/python-dotenv/) package; or
2. Through saving the keys in a gitignored `credentials/` folder and
reading it from the local file.

## The web-service API

The code for the web app can be found in the `api/` folder.

At the time of creation, I choose Python
[Flask](https://flask.palletsprojects.com/en/2.0.x/) for the web
service framework. Nowadays, it might be wise to consider
[FastAPI](https://fastapi.tiangolo.com/) as an alternative when you want to
continue with my work or start your own web service.

The app is fully deployed and run on [Free Tier](https://cloud.google.com/free)
products of Google Cloud. This means that with limited usage, the hosting of
the website and webservice cost nothing.

[App Engine](https://cloud.google.com/appengine/docs/python) is used for
deploying the Flask App. App Engine is an easy to use serverless application,
meaning that the apps scales automatically to meet traffic demand. I have also
considered Cloud Functions, but I found that App Engine is a bit more flexible
in terms of customizing the application infrastructure.

Furthermore, I initially used Google's NoSQL cloud database
[Cloud Firestore](https://cloud.google.com/firestore) to fetch place
information from (also a Free Tier product), but as my dataset turned out to
be limited in size, it is simply faster to upload the data to the App Engine
and serve recommendations directly from there without connecting to a separate
database.

The `notebooks/api/google-firestore/` folder still contains several notebooks
with examples on how to load and retrieve data with Cloud Firestore. I make an
assessment on whether Firestore is fit for purpose in
`querying-firestore.ipynb` and conclude that it's not suited for my use case.

## Data Preparation

The code for all data preparation can be found in the `scripts/`, `notebooks/`
and `src/` folders.


## TODO

[ ] Add LICENSE?
[ ] Review folder structure
[ ] Decide which data to check in + Empty folders to keep in data folder
[ ] Checking local paths in scripts (users/terminator)
