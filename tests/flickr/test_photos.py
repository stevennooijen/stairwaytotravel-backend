from typing import Dict, Union

import pytest
from pandas import DataFrame, Series

from stairway.apis.flickr.photos import (
    create_attribution_url,
    create_image_url,
)


def test_get_attribution_url() -> None:
    """
    Expect correct creation of attribution url.
    """
    expected = "https://www.flickr.com/photos/7679455@N03/3970594887"

    test_input = Series({"owner": "7679455@N03", "id": "3970594887"})

    assert expected == create_attribution_url(test_input)


@pytest.mark.parametrize(
    "item",
    [
        {
            "farm": 3,
            "id": "3970594887",
            "secret": "fbdbd8dbaa",
            "server": "2601",
        },
        Series(
            {
                "farm": 3,
                "id": "3970594887",
                "secret": "fbdbd8dbaa",
                "server": "2601",
            }
        ),
    ],
)
def test_get_image_url(item: Union[Dict, Series]) -> None:
    """
    Expect correct creation of image url.
    """
    expected = (
        "https://farm3.staticflickr.com/2601/3970594887_fbdbd8dbaa_b.jpg"
    )

    assert expected == create_image_url(item)


def test_get_image_url_dataframe() -> None:
    """
    Expect correct vectorized creation of image url for each DataFrame row.
    """
    expected = Series(
        [
            "https://farm3.staticflickr.com/2601/3970594887_fbdbd8dbaa_b.jpg",
            "https://farm66.staticflickr.com/65535/"
            + "49723281427_34018c9501_b.jpg",
        ]
    )

    test_df = DataFrame(
        [
            {
                "farm": 3,
                "id": "3970594887",
                "secret": "fbdbd8dbaa",
                "server": "2601",
            },
            {
                "farm": 66,
                "id": "49723281427",
                "secret": "34018c9501",
                "server": "65535",
            },
        ]
    )

    assert expected.equals(create_image_url(test_df))
