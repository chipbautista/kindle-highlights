from typing import List

import streamlit as st

import ui_utils
from src.db.base import Highlight


def book_selector(books, book_index) -> int:
    selected_book_index = st.selectbox(
        "Select Book",
        book_index,
        format_func=lambda x: ui_utils.format_book_title(books[x]),
    )
    return selected_book_index


def show_highlights(highlights_to_display: List[Highlight]) -> None:
    for i, highlight in enumerate(highlights_to_display):
        datetime_formatted = ui_utils.format_datetime(highlight.datetime)
        st.markdown(f"##### #{i + 1}")

        st.markdown(f"{highlight.text}")
        if highlight.note:
            st.markdown(f"*{highlight.note}*")

        st.markdown(
            f'<font color="grey">*{datetime_formatted}*</font>', unsafe_allow_html=True
        )
        st.markdown("---")


def show_book_metadata(book):
    if book.google_metadata:
        metadata = book.google_metadata[0]
        img_col, metadata_col = st.columns(2)
        with img_col:
            st.image(metadata.cover_image)
        with metadata_col:
            st.markdown(f"### {metadata.title}")
            st.markdown(f"#### *{metadata.subtitle}*")
            st.markdown(f"Published {metadata.published_date}")
            st.markdown(f"Categories: {metadata.categories}")

        with st.expander("Show synopsis"):
            st.markdown(metadata.description)
