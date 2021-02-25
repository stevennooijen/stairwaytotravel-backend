from io import BytesIO
from pathlib import Path
from typing import Tuple, Union

import requests
from PIL import Image, ImageDraw, ImageFont

# defaults
INPUT_FOLDER = Path(__file__).parent / "utils"
LOGO_LAYER_PATH = INPUT_FOLDER / "logo-darkened-bottom.png"
PLACE_FONT_PATH = INPUT_FOLDER / "Roboto-Bold.ttf"
COUNTRY_FONT_PATH = INPUT_FOLDER / "Roboto-Regular.ttf"


def create_instagram_image(
    image_path: str,
    place_text: str,
    country_text: str,
    output_path: str = None,
    logo_layer_path: Union[Path, str] = LOGO_LAYER_PATH,
    place_font_path: Union[Path, str] = PLACE_FONT_PATH,
    country_font_path: Union[Path, str] = COUNTRY_FONT_PATH,
) -> Image:
    """
    Format an image from file or url to the Stairway Instagram post format.

    Parameters
    ----------
    image_path: str
        Local path or url referring to the original image to format.
    place_text: str
        Name of the place to put on the image.
    country_text: str
        Name of the country to put on the image.
    output_path: str
        Output path to save the created image. If None, don't save.
    logo_layer_path: str
        Path to the logo layer to apply to the image.
    place_font_path: str
        Path to the font to use for place_text.
    country_font_path: str
        Path to the font to use for country_text.

    Returns
    -------
    out: Image
        Formatted image.
    """
    if image_path[0:4] == "http":
        response = requests.get(image_path)
        image = Image.open(BytesIO(response.content))
    else:
        image = Image.open(image_path)

    # resize and crop
    image = resize_image(image)
    image = crop_image_center(image)

    # logo layer
    logo = Image.open(logo_layer_path)
    # don't need to provide position as both are already 1080x1080
    image.paste(logo, mask=logo)

    # text layer
    add_text_to_image(image, place_text, (210, 870), str(place_font_path), 80)
    add_text_to_image(
        image, country_text, (210, 962), str(country_font_path), 40
    )

    if output_path:
        image.save(output_path, optimize=True, quality=90)

    return image


def resize_image(image: Image, smallest_dimension: int = 1080):
    """
    Resize the smallest dimension of an image to the length specified while
    maintaining the image aspect ratio.
    """
    width, height = image.size  # Get dimensions

    if height > width:
        new_height = int(smallest_dimension * height / width)
        new_width = smallest_dimension
    else:
        new_height = smallest_dimension
        new_width = int(smallest_dimension * width / height)

    return image.resize((new_width, new_height))


def crop_image_center(image: Image, crop_size: Tuple[int, int] = (1080, 1080)):
    """
    Crop and return the center of the image of dimensions `crop_size`.
    """
    new_width, new_height = crop_size

    width, height = image.size  # Get dimensions

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    # Crop the center of the image
    return image.crop((left, top, right, bottom))


def add_text_to_image(
    image, text, coordinates, font, size, color="rgb(255, 255, 255)"
):
    """
    Add text to an image.
    """
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, size=size)
    (x, y) = coordinates
    draw.text((x, y), text, fill=color, font=font)
