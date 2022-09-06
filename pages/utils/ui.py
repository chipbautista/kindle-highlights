from typing import List

import streamlit as st

from src.db.base import Highlight, Book


def format_book_title(book: Book):
    return f"{book.title} ({book.author.name})"


def format_datetime(x: str) -> str:
    return x.strftime("%B %d, %Y %I:%M %p")



def show_highlight(highlight: Highlight, i: int, show_book_title: bool = False):
    datetime_formatted = format_datetime(highlight.datetime)
    st.markdown(f"##### #{i + 1}")

    st.markdown(f"{highlight.text}")
    if show_book_title:
        st.markdown(f"*{highlight.book.title} ({highlight.book.author.name})*")
    if highlight.note:
        st.markdown(f"*{highlight.note}*")

    st.markdown(
        f'<font color="grey">*{datetime_formatted}*</font>', unsafe_allow_html=True
    )
    st.markdown("---")
