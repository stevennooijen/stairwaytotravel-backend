from typing import Dict, List

import requests


def get_wikivoyage_page_info(page_ids: List[int]) -> Dict:
    """
    Query wikivoyage page info using the wikivoyage internal id.
    """
    S = requests.Session()

    params = {
        "origin": "*",
        "action": "query",
        "format": "json",
        "prop": "info",
        "inprop": "url",
        "pageids": "|".join([str(page_id) for page_id in page_ids]),
    }

    R = S.get(url="https://en.wikivoyage.org/w/api.php?", params=params,)
    return R.json()["query"]["pages"]
