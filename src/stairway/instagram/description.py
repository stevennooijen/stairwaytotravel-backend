import random
import string


def create_draft_description(place, country, author):
    text = f"""<Text here>

👉 Link to place in bio
📸 Photo by @{author} on Flickr

#{clean_text(place)} #{clean_text(country)} {pick_generic_hastags()} #stairwaytotravel"""
    return text


def pick_generic_hastags(nr_hashtags=9):
    hashtags = [
        "#instatravel",
        "#beautifuldestinations",
        "#trip",
        "#traveltime",
        "#worldtour",
        "#traveltheworld🌍",
        "#epic",
        "#adventuretime",
        "#traveltheworld",
        "#vacationgoals",
        "#traveladdict",
        "#seetheworld",
        "#allaboutadventures",
        "#traveldeeper",
        "#travellife",
        "#travelawesome",
        "#travel",
        "#travelphoto",
        "#adventure",
        "#travellust",
        "#vacation",
        "#travelphotography",
        "#inspiration",
        "#discover",
        "#travelfreak",
        "#worldwide_moods",
        "#goodvibes",
        "#beautifulplaces",
        "#traveldestination",
        "#travellingthroughtheworld",
        "#wanderlust",
        "#explore",
        "#globetrotter",
        "#travelphotography📷",
        "#wanderer",
        "#travelgram",
        "#picturesque",
        "#travelbug",
        "#special_shots",
        "#worldplaces",
        "#exploretheworld",
    ]
    return " ".join(random.sample(hashtags, nr_hashtags))


def clean_text(text: str) -> str:
    return (
        text.translate(str.maketrans("", "", string.punctuation))
        .replace(" ", "")
        .lower()
    )
