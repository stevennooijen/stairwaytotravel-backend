from stairway.flickr.photos import get_attribution_url


def test_get_attribution_url():
    """
    Expect correct creation of attribution url.
    """
    expected = "https://www.flickr.com/photos/7679455@N03/3970594887"

    test_input = {
        "owner": "7679455@N03",
        "id": "3970594887",
    }

    assert expected == get_attribution_url(test_input)
