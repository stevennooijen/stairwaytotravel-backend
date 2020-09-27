from typing import Tuple

import pytest
from PIL import Image
from stairway.instagram.image import resize_image


@pytest.mark.parametrize(
    "input_size,length,expected",
    [
        ((60, 20), 10, (30, 10)),
        ((20, 60), 5, (5, 15)),
        ((1000, 500), 1080, (2160, 1080)),
    ],
)
def test_resize_image(
    input_size: Tuple[int], length: int, expected: Tuple[int]
) -> None:
    """
    Expect correct output size of the test image.
    """
    test_img = Image.new("RGB", input_size, color="red")

    assert expected == resize_image(test_img, smallest_dimension=length).size
