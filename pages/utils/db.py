from typing import List

import streamlit as st

from src.db.base import Book, Highlight
from src.db.session import get_db
from .s3 import download_from_s3


ENV = st.secrets.get("ENV", "dev")


def get_app_db():
    if ENV == "dev":
        db = get_db()
    else:
        db_file = download_from_s3("db", st.secrets["aws"])
        db = get_db(db_url=f"sqlite:///{db_file}")
    return db


# @st.cache -- cached outputs will be detached objects from DB
def get_books():
    db = get_app_db()
    books = db.query(Book).all()
    return books


def get_highlights() -> List[Highlight]:
    db = get_app_db()
    highlights = db.query(Highlight).all()
    return highlights


def search_highlights(query: str) -> List[Highlight]:
    if query:
        db = get_app_db()
        result = db.query(Highlight).filter(Highlight.text.contains(query)).all()
        # to-do: pagination
        return result[:50]
    return []
