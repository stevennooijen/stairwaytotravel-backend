import requests

IMAGES_PER_PAGE = 5
API_BASE = "https://api.flickr.com/services/rest/?method=flickr.photos.search"
FORBIDDEN_WORDS = [
    "police",
    "car",
    "truck",
    "bus",
    "transport",
    "transportation",
    "metro",
    "train",
    "trains",
    "localtrain",
    "trein",
    "keteltrein",
    "rail",
    "railroad",
    "railway",
    "railways",
    "railogix",
    "railrunner",
    "captrain",
    "CSXT",
    "HSL",
    "GNWR",
    "goederen",
    "locomotive",
    "plane",
    "air",
    "airplane",
    "airline",
    "airways",
    "aircraft",
    "airport",
    "vessel",
    "ship",
    "fleet",
    "freight",
    "marine",
    "pano",
    "panorama",
    "microphotography",
    "product",
    "investment",
    "affairs",
    "embassy",
    "minister",
    "candidate",
    "president",
    "meeting",
    "conference",
    "manager",
    "defense",
    "defence",
    "force",
    "department",
    "guard",
    "navy",
    "naval",
    "military",
    "fighter",
    "gun",
    "attack",
    "emergency",
    "fire",
    "burning",
    "smoke",
    "brigade",
    "map",
    "selfie",
    "selfportrait",
    "insect",
    "bird",
    "model",
    "sexy",
    "shirtless",
    "fashion",
    "archeon",
    "anime",
    "design",
    "store",
    "singer",
    "flower",
    "plant",
    "galaxy",
    "astronomy",
    "stars",
    "cat",
    "katzen",
    "dog",
    "labrador",
    "buddies",
    "christmas",
    "eneq",
    "EVS",
]


def get_flickr_images(
    search_string,
    api_key,
    images_per_page=IMAGES_PER_PAGE,
    forbidden_words=FORBIDDEN_WORDS,
):
    """Call on flickr.photos.search. Returns json list of images satisfying the params."""
    S = requests.Session()

    params = {
        "api_key": api_key,
        "format": "json",
        "nojsoncallback": 1,
        "per_page": images_per_page,
        "sort": "interestingness-desc",
        "safe_search": 1,
        "license": "4,5,7,8,9,10",
        "content_type": 1,
        "media": "photos",
        "extras": "owner_name,url_o,original_format",
        "text": search_string + " -" + " -".join(forbidden_words),
    }

    R = S.get(url=API_BASE, params=params)
    return R.json()["photos"]


def get_image_url(item, suffix="_b"):
    """Construct url for downloading the image. Add suffix '_b' for large size."""
    return (
        "https://farm"
        + item["farm"].astype(str)  # hacky to make it work for pandas df assign
        # + str(item['farm'])
        + ".staticflickr.com/"
        + item["server"]
        + "/"
        + item["id"]
        + "_"
        + item["secret"]
        + suffix
        + ".jpg"
    )


def get_attribution_url(item):
    """Assemble an attribution link from fetched photos.search result."""
    return "https://www.flickr.com/photos/" + item["owner"] + "/" + item["id"]
