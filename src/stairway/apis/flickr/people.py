import xml.etree.ElementTree as ET
from typing import Dict

import requests


def get_flickr_people_info(user_id: str, api_key: str,) -> str:
    """
    Returns xml string with people info from flickr.people.getInfo API.
    """
    S = requests.Session()

    params = {"api_key": api_key, "user_id": user_id}

    R = S.get(
        url="https://api.flickr.com/services/rest/?method=flickr.people.getInfo",
        params=params,
    )

    return R.content


def parse_flickr_people_info(xml_string: str) -> Dict:
    """
    Parse Dict with relevant people info from flickr.people.getInfo xml string.
    """
    response_xml = ET.fromstring(xml_string)
    person = response_xml.find("person")

    if person:
        people_info = {
            field: person.find(field).text
            for field in ["username", "realname", "profileurl", "location"]
            if person.find(field) is not None
        }
        people_info["nsid"] = person.get("nsid")
        people_info["path_alias"] = person.get("path_alias")
    else:
        people_info = {}

    return people_info
