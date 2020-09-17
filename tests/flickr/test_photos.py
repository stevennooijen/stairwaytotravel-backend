from typing import Dict, Union
from pandas import Series
import pytest

from stairway.flickr.photos import get_attribution_url, get_image_url


def test_get_attribution_url() -> None:
    """
    Expect correct creation of attribution url.
    """
    expected = "https://www.flickr.com/photos/7679455@N03/3970594887"

    test_input = Series({"owner": "7679455@N03", "id": "3970594887",})

    assert expected == get_attribution_url(test_input)


@pytest.mark.parametrize(
    "item",
    [
        {"farm": 3, "id": "3970594887", "secret": "fbdbd8dbaa", "server": "2601",},
        Series(
            {"farm": 3, "id": "3970594887", "secret": "fbdbd8dbaa", "server": "2601",}
        ),
    ],
)
def test_get_image_url(item: Union[Dict, Series]) -> None:
    """
    Expect correct creation of image url.
    """
    expected = "https://farm3.staticflickr.com/2601/3970594887_fbdbd8dbaa_b.jpg"

    assert expected == get_image_url(item)
