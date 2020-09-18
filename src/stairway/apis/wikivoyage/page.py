from typing import Dict

import requests


def get_wikivoyage_page_info(page_id: int) -> Dict:
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
        "pageids": page_id,
    }

    R = S.get(url="https://en.wikivoyage.org/w/api.php?", params=params,)
    return R.json()["query"]["pages"][str(page_id)]
