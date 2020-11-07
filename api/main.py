import pandas as pd
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources.destination import Destination
from resources.explore import Explore
from resources.nearby import Nearby
from resources.member import Member
from resources.signup import Signup

app = Flask(__name__)
CORS(
    app,
    origins=[
        "https://stairwaytotravel.com",
        "https://stairwaytotravel.web.app",
        "https://stairwaytotravel.firebaseapp.com",
        "https://stairwaytotravel-release.web.app",
        "https://stairwaytotravel-release.firebaseapp.com",
        "http://localhost:3000",
    ],
)
api = Api(app)

MAILCHIMP_KEY = "credentials/mailchimp-key.json"

# load data once
df = (
    pd.read_csv("./data/wikivoyage_destinations.csv")
    .set_index("id", drop=False)
)
df_features = pd.read_csv("./data/wikivoyage_features.csv").set_index("id")
df_feature_types = pd.read_csv("./data/wikivoyage_features_types.csv")

# Api for fetching destinations
api.add_resource(
    Destination,
    "/api/",
    resource_class_kwargs={
        "df": df,
        "df_features": df_features,
        "df_feature_types": df_feature_types,
    },
)
api.add_resource(
    Destination,
    "/api/<dest_id>",
    endpoint="dest_ep",
    resource_class_kwargs={
        "df": df,
        "df_features": df_features,
        "df_feature_types": df_feature_types,
    },
)
api.add_resource(
    Explore,
    "/api/explore/",
    resource_class_kwargs={
        "df": df,
        "df_features": df_features,
        "df_feature_types": df_feature_types,
    },
)
api.add_resource(
    Nearby,
    "/api/nearby/<dest_id>",
    resource_class_kwargs={
        "df": df,
    },
)

# Api for email signup form
api.add_resource(
    Signup, "/signup/", resource_class_kwargs={"mailchimp-key": MAILCHIMP_KEY, "df": df}
)
api.add_resource(
    Member,
    "/member/",
    resource_class_kwargs={"mailchimp-key": MAILCHIMP_KEY, "df": df},
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
