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
