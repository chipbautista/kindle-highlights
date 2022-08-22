import streamlit as st

from src.db.base import Book
from src.db.session import get_db


# @st.cache
def get_books():
    db = get_db()
    books = db.query(Book).all()
    return books
