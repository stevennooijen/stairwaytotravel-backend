from typing import Dict, Union, List
import requests
from pandas import Series, DataFrame

IMAGES_PER_PAGE = 5
LICENSES = "4,5,7,8,9,10"
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
    "abstract",
    "minimal",
    "repetition",
    "repeat",
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
    search_string: str,
    api_key: str,
    images_per_page: int = IMAGES_PER_PAGE,
    forbidden_words: List[str] = FORBIDDEN_WORDS,
    license: str = LICENSES,
) -> Dict:
    """
    Call on flickr.photos.search API. Returns json list of images satisfying the params.
    """
    S = requests.Session()

    params = {
        "api_key": api_key,
        "format": "json",
        "nojsoncallback": 1,
        "per_page": images_per_page,
        "sort": "interestingness-desc",
        "safe_search": 1,
        "license": license,
        "content_type": 1,
        "media": "photos",
        "extras": "owner_name,url_o,original_format",
        "text": search_string + " -" + " -".join(forbidden_words),
    }

    R = S.get(
        url="https://api.flickr.com/services/rest/?method=flickr.photos.search",
        params=params,
    )
    return R.json()["photos"]


def create_image_url(item: Union[Dict, Series, DataFrame], suffix: str = "_b") -> str:
    """
    Construct url for downloading the image. Add suffix '_b' for large size.
    """
    return (
        "https://farm"
        + (
            item["farm"].astype(str)
            if isinstance(item, DataFrame)
            else str(item["farm"])
        )
        + ".staticflickr.com/"
        + item["server"]
        + "/"
        + item["id"]
        + "_"
        + item["secret"]
        + suffix
        + ".jpg"
    )


def create_attribution_url(item: Union[Dict, Series]) -> str:
    """
    Assemble an attribution link from fetched photos.search result.
    """
    return "https://www.flickr.com/photos/" + item["owner"] + "/" + item["id"]
