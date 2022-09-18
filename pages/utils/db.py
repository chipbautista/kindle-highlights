from typing import List

import pandas as pd
import streamlit as st
from sqlalchemy import func

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


def get_highlights(
    sort_by_recency: bool = False, date_range: tuple = (), with_notes_only: bool = False
) -> List[Highlight]:
    db = get_app_db()
    query = db.query(Highlight)

    if len(date_range) >= 1:
        min_date = date_range[0]
        query = query.filter(Highlight.datetime >= min_date)

    if len(date_range) == 2:
        max_date = date_range[1]
        query = query.filter(Highlight.datetime <= max_date)

    if with_notes_only:
        query = query.filter(Highlight.note.isnot(None))

    if sort_by_recency:
        query = query.order_by(Highlight.datetime.desc())

    highlights = query.all()
    return highlights


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


def get_min_max_highlight_dates(db=None):
    if db is None:
        db = get_app_db()

    min_date = db.query(func.min(Highlight.datetime)).one()[0]
    max_date = db.query(func.max(Highlight.datetime)).one()[0]
    return min_date, max_date
