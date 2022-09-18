import _thread
import weakref
from typing import List

import pandas as pd
import streamlit as st

from src.db.base import Book, Highlight
from src.db.session import get_db
from .s3 import download_from_s3


ENV = st.secrets.get("ENV", "dev")


def get_app_db():
    if ENV == "dev":
        db = get_db()
    else:
        db_file = download_from_s3(st.secrets["aws"]["DB_FILE"])
        db = get_db(db_url=f"sqlite:///{db_file}")
    return db


def get_books():
    db = get_app_db()
    books = db.query(Book).all()
    return books


def get_highlights() -> List[Highlight]:
    db = get_app_db()
    highlights = db.query(Highlight).all()
    return highlights


@st.cache(
    allow_output_mutation=True,
    hash_funcs={_thread.RLock: lambda _: None, weakref.ReferenceType: lambda _: None},
)
def get_highlights_series() -> pd.Series:
    highlights = get_highlights()
    highlights_ = pd.Series(highlights, name="highlight_db_obj")
    highlights_.index = [h.text for h in highlights]
    return highlights_


def search_highlights(query: str) -> List[Highlight]:
    if query:
        db = get_app_db()
        result = db.query(Highlight).filter(Highlight.text.contains(query)).all()
        # to-do: pagination
        return result[:50]
    return []
