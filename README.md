# Stairway to Travel: Backend

[Stairway to Travel](https://stairwaytotravel.com/) offers personalized travel
recommendations that help you shape unique itineraries.

Stairway to Travel has long been my dream project with the aspiration of
becoming a profitable business. Now, I am donating my code to the community
that I have benefitted of so much in the creation of this website. I hope you
will learn or benefit from what I did. Please feel free to reach out in case
of questions or remarks!

Read the full story about why I am open sourcing everything in
[my blog](https://stairwaytotravel.com/blog/why-open-source-and-lessons-learned).

## About this repo

This is the code repository containing backend related services for Stairway
to Travel. The repository's goal is to version control code related to:

1. The backend web-service API hosted on Google Cloud Platform (GCP).
2. Analysis and preparation of various data sources.
3. One-off analyses, for example for marketing purposes.

The frontend code for Stairway to Travel's user interface can be found in the
related repository named
[stairwaytotravel-frontend](https://github.com/stevennooijen/stairwaytotravel-frontend).

### Folder structure

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

### Preparing your working environment

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

### Credentials

Several scripts and functions require credentials to access third party APIs
like Flickr, Mailchimp or Google App Engine. These keys have not been uploaded
to Git and you will have to get your own keys for access to these tools.

Retrieval of the keys happens in two ways:

1. Either through a `.env` file using the
   [`python-dotenv`](https://pypi.org/project/python-dotenv/) package; or
2. Through saving the keys in a gitignored `credentials/` folder and
   reading it from the local file.

## 1. The web-service API

The code for the web app can be found in the `api/` folder, which includes the
`api/README.md` file with detailed instructions on how to run the API server.

Please find below a high level architecture of the application. Read more about
each component in the remainder of this section.

![Application architecture](/documentation/architecture/stairway-architecture.png)

### The Flask app

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

### Ping service

The downside of a serverless offering is a bit of request and response latency
during the time when your app's code is being loaded to a newly created
instance. Although this can be completely avoided by always having a machine up
and running, this would also incur costs. To stay within the Free Tier, I use
Cloud Functions and Cloud Scheduler to regularly ping my App Engine instance
so that the machine will be kept 'alive'. By doing so every 10 minutes, I found
an ideal balance between possible latency and costs on the other hand.

### The database

I initially used Google's NoSQL cloud database
[Cloud Firestore](https://cloud.google.com/firestore) to fetch place
information from (also a Free Tier product). However, as my dataset turned out
to be limited in size, it is simply faster to upload the data to the App Engine
and serve recommendations directly from there without connecting to a separate
database. The Cloud Firestore component in the architecture diagram above is
therefore no longer in use.

The `notebooks/api/google-firestore/` folder still contains several notebooks
with examples on how to load and retrieve data with Cloud Firestore. I make an
assessment on whether Firestore is fit for purpose in
`querying-firestore.ipynb` and conclude that it's not suited for my use case.

### Mailchimp

Mailchimp is used for email automation whenever users sign up for newsletters
or when they check-out with their bucket list of places they want to visit.

Details on the designed architecture and workflow automation can be found in
the `documentation/mailchimp/` folder.

## 2. Data Preparation

The second function of this repository is to prepare data for use in the
recommendation service. Over time, I have investigated many different datasets
and I have often done so in Jupyter notebooks. Hence, the code for data
preparation is a bit more messy then for the API and the code is spread over
the `scripts/`, `notebooks/` and `src/` folders.

A diagram with a detailed approach on how to clean and combine data can be
found in the `documentation/data-processing/` folder. In general, data prep
follows the following phases wherein intermediate data is stored locally in
the `data/` folder:

1. **Raw**: a copy from the source as-is in its original format
2. **Clean**: transformed data in a easy to handle CSV format
3. **Processed**: feature extraction on the cleaned data
4. **Enriched**: cleaned datasets are combined into their final shape
5. **API Data**: data for the API is copied into the `api/data/` folder so that
   it will be uploaded to Google App Engine when deploying the Flask app.

To get your own copy of raw data, follow the instructions below:

| Source                 | Data type        | How to get it                                                                             |
| ---------------------- | ---------------- | ----------------------------------------------------------------------------------------- |
| Wikivoyage             | Place info       | Download latest `.xml.bz2` files [here](https://dumps.wikimedia.org/enwikivoyage/latest/) |
| Wikivoyage             | Page info        | Public API, run script `wikivoyage_page_info.py`                                          |
| Wikivoyage             | Place activities | Feature extraction with BM25. See `features-bm25.ipynb`                                   |
| University of Delaware | Weather          | Download `.nc` files [here](https://psl.noaa.gov/data/gridded/data.UDel_AirT_Precip.html) |
| Visual Crossing        | Weather          | Paid API, run script `visualcrossing_monthly_weather_threaded.py`                         |
| Flickr                 | Place images     | Private API, run script `flickr_image_list`                                               |
| Flickr                 | People info      | Private API, run script `flickr_people_list`                                              |
| Geonames               | Place info       | Download `.zip` files [here](https://download.geonames.org/export/dump/)                  |

With the above instructions you should be able to replicate all data sets. The
final data that is used in the API service is the only data that I checked in,
see the `api/data/` folder.

## 3. One-off Analyses

On occassions I did a one-off analysis that isn't quite related to data prep or
the backend API service. For example, for marketing purposes, I retrieved
the top 5 Flickr images per place and formatted them automatically into the
standard square Instagram format with a text and logo. See the result on
Stairway to Travel's
[Instagram profile](https://www.instagram.com/stairwaytotravel/). I also made a
[rotating globe](https://www.youtube.com/watch?v=B7IMcWXfJL8) depicting which
places I already covered on Instagram.

Code for these things can be found partly in `notebooks/one-off-analyses/`.

## TODO

When I was still actively working on this project I kept a huge list of tasks
with new and improved functionality in Trello. In case you are curious or are
considering to continue this project, feel free to have a look at the
[frontend repository's issues](https://github.com/stevennooijen/stairwaytotravel-frontend/issues)
. I labelled tasks that require backend work with a 'backend' label.
