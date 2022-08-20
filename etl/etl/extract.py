from re import search

import pandas as pd
from dagster import op

from .utils import get_latest_clippings_file


@op(config_schema={"clippings_file": str})
def read_clippings(context) -> str:
    clippings_file = context.op_config["clippings_file"] or get_latest_clippings_file()
    context.log.info(f"Clippings file to process: '{clippings_file}'")
    clippings_text = _read_clippings(clippings_file)

    return clippings_text


def _read_clippings(clippings_file: str) -> str:
    with open(clippings_file, "r", encoding="utf-8") as f:
        clippings = f.read().strip()
        # Remove the byte order marks
        clippings = clippings.replace("\ufeff", "")
    return clippings
