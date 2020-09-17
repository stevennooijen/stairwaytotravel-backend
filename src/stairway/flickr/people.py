import xml.etree.ElementTree as ET

import requests


def get_flickr_people_info(
    user_id, api_key,
):
    """Call on flickr.photos.search. Returns json list of images satisfying the params."""
    S = requests.Session()

    params = {"api_key": api_key, "user_id": user_id}

    R = S.get(url=API_BASE + "?method=flickr.people.getInfo", params=params)

    return R.content


def parse_flickr_people_info(xml_string):
    """Retrieve relevant people info from API returned xml. """
    response_xml = ET.fromstring(xml_string)

    people_info = {
        field: response_xml.find("person").find(field).text
        for field in ["username", "realname", "profileurl"]
    }
    people_info["path_alias"] = response_xml.find("person").get("path_alias")

    return people_info
