from datetime import datetime
from pathlib import Path
from os.path import getmtime
from dotenv import dotenv_values


ENV_VARS = dotenv_values(".env")


def get_latest_clippings_file() -> str:
    clippings_folder = ENV_VARS["DEFAULT_CLIPPINGS_FOLDER"]
    latest_file = sorted(Path(clippings_folder).iterdir(), key=getmtime)[-1]
    return str(latest_file)


def parse_date(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%B %d, %Y %I:%M:%S %p")
