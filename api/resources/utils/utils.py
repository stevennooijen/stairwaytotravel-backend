def create_stairwaytotravel_url(place_id):
    """Create a url to a place page given the place id."""
    return "https://stairwaytotravel.com/explore/" + str(place_id)


def create_html_link(url, text):
    """Wrap a text into an html anchor element with a specified url."""
    line = f"<a href='{url}'>{text}</a>"
    return line


def create_one_list_item(
    df_in, place_id, line_prefix="<li>", line_postfix="", add_link=False
):
    """Create one line of text for a given place.

    Parameters
    ----------
    df_in: DataFrame
        DataFrame to look up the place_id in.
    place_id: int
        Unique id for the place to generate the line of text for.
    line_prefix: str
        Start each line with this string.
    line_postfix: str
        End each line with this string.
    add_link: bool
        Whether to wrap the text in an html anchor element.
    Returns
    -------
    str
        A line of text about the specified place.
    """
    record = df_in.loc[lambda df: df["id"] == place_id]
    text = record["name"].iloc[0] + ", " + record["country"].iloc[0]
    link = create_html_link(create_stairwaytotravel_url(place_id), text)
    line = line_prefix + (link if add_link else text) + line_postfix
    return line


def create_list_of_likes(
    df_in, likes, list_prefix="<ul>", list_postfix="</ul>", **kwargs
):
    """Create a string listing the specified liked places.

    Parameters
    ----------
    df_in: DataFrame
        DataFrame to look up the place_id in.
    likes: list
        List with unique ids for the places to create the text for.
    list_prefix: str
        Start the list with this string.
    list_postfix: str
        End the list with this string.
    Returns
    -------
    str
        A string listing the specified places.
    """
    output = list_prefix
    for like in likes:
        output = output + create_one_list_item(df_in, like, **kwargs)
    output = output + list_postfix
    return output


def split_text_in_chuncks(text, max_characters=255, split_character=">"):
    """Generator that chops a text into parts that end with a certain character.

    Parameters
    ----------
    text: str
        Input string to be split into parts.
    max_characters: int
        Maximum length of one part.
    split_character: str
        Character that each part should end with.
    Returns
    -------
    iterator
        Generator that yields parts of the string.
    """
    remaining_text = text
    while True:
        next_part = remaining_text[0:max_characters]
        index_in_chunck = next_part.rfind(split_character)
        if index_in_chunck < 0:
            break
        yield remaining_text[0 : index_in_chunck + 1]
        remaining_text = remaining_text[index_in_chunck + 1 :]


def pad_or_truncate_list(some_list, target_len=21, pad_value=""):
    """Pads (with a value) or truncates list to a target length.

    Parameters
    ----------
    some_list: list
        Input list to pad or truncate.
    target_len: int
        Length of the desired output list.
    pad_value: anything
        Value to pad with if the input length needs to be extended.
    Returns
    -------
    list
        Padded or truncated list of target length.
    """
    return some_list[:target_len] + [pad_value] * (target_len - len(some_list))


def prettify_n_results(n):
    thresholds = [300, 1000, 5000, 10000, 20000]
    if n > 300:
        n = (
            "{:,}".format(
                (max([result for result in thresholds if n > result]))
            ).replace(",", ".")
            + "+"
        )
    return n


def add_normalized_column(df, column_name):
    """
    Normalize a column and add it to the DataFrame.

    Parameters
    ----------
    df: DataFrame
        Input DataFrame containing the column to normalize.
    column_name: string
        Name of the column to normalize.

    Returns
    -------
    out: DataFrame
        DataFrame with a normalized column having postfix "_norm".
    """
    df[f"{column_name}_norm"] = (df[column_name] - df[column_name].min()) / (
        df[column_name].max() - df[column_name].min()
    )
    return df
