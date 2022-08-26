from typing import Tuple
from re import search, findall

import pandas as pd
import numpy as np
from loguru import logger
from dagster import op

from . import utils


@op
def transform_clippings_to_dataframe(context, clippings_text: str) -> pd.DataFrame:

    # this seems to be a reliable way to split each entry in kindle's Clippings file
    docs = clippings_text.split("==========")

    parsed_docs = [parse_document(doc) for doc in docs]
    docs_df = pd.DataFrame.from_records(parsed_docs).dropna(how="all")

    docs_df[["Book Title", "Author"]] = pd.DataFrame.from_records(
        docs_df["doc_title"].apply(parse_title_and_author)
    )

    docs_df["datetime"] = docs_df["date"].apply(utils.parse_date)

    docs_df = connect_notes_to_highlights(docs_df)
    docs_df = docs_df[docs_df["type"] == "Highlight"].copy()
    docs_df = drop_duplicate_highlights(docs_df)

    return docs_df


def parse_document(doc: str) -> dict:
    doc = doc.strip()
    if not doc:
        return {}

    data = {}
    lines = doc.split("\n")

    data = {
        "doc_title": lines[0],
        "type": search(r"Your\s([A-Za-z]+)\s", lines[1]).group(1),
        "location": search(r"Location ([\d\-]+)", lines[1]).group(1),
        "date": search(r"Added on [A-Za-z]+, (.+)$", lines[1]).group(1),
        "text": lines[3] if len(lines) > 2 else np.nan,
    }
    return data


def parse_title_and_author(string: str) -> Tuple[str, str]:
    # Separate title and author from strings in this format: "Title (Author)"
    try:
        # author is likely to be the text inside the last parenthesis
        author = findall(r"\(([A-Za-z,\.; ]+)\)", string)[-1]
        title = string.replace(f"({author})", "")

        try:
            last_name, first_name = author.split(",")
            author = f"{first_name} {last_name}"
        except ValueError:
            pass

        return title.strip(), author.strip()

    except Exception as e:
        logger.warning(f"Cannot parse title and author from '{string}'. {e}")
        return string, "Unknown"


def drop_duplicate_highlights(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates that are caused by repeated highlighting on Kindle touch screen
    -- like when you weren't able to select the text you want so you delete the current highlight and try again"""
    indices = df.index
    for i, index in enumerate(indices[:-1]):
        curr_text = df.loc[index, "text"]
        next_text = df.loc[indices[i + 1], "text"]

        if next_text.startswith(curr_text) or curr_text.startswith(next_text):
            df.drop(index=index, inplace=True)

    return df


def connect_notes_to_highlights(docs_df: pd.DataFrame) -> pd.DataFrame:
    docs_df["location_end"] = docs_df["location"].apply(lambda x: x.split("-")[-1])

    # TODO: optimize this for loop by using index assignment instead
    notes = docs_df[docs_df["type"] == "Note"]
    for _, note in notes.iterrows():
        # Get the highlight which the note is referring to.
        highlight_idx = docs_df[
            (docs_df["doc_title"] == note["doc_title"])
            & (docs_df["location_end"] == note.location)
        ].index[0]

        # add this note to that highlight
        docs_df.loc[highlight_idx, "Note"] = note.text

    # remove temp column and notes
    docs_df = docs_df.drop(columns=["location_end"], index=notes.index)
    return docs_df
