import pytest
from stairway.instagram.description import clean_text


@pytest.mark.parametrize(
    "input_text,expected",
    [("'s-Gravenhage", "sgravenhage"), ("Den Bosch", "denbosch"),],
)
def test_clean_text(input_text: str, expected: str,) -> None:
    """
    Expect strings to be correctly cleaned.
    """
    assert expected == clean_text(input_text)
