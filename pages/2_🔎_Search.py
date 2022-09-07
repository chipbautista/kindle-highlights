from typing import List, Set
from re import sub, IGNORECASE

import streamlit as st
import pandas as pd

from src.models.highlight import Highlight
from pages.utils.db import search_highlights
from pages.utils.ui import show_highlight

st.write("## Highlight Search")


def highlight_search_query(text: str) -> str:
    return sub(
        rf"({query})",
        "<mark style='background-color: yellow;'>\\1</mark>",
        text,
        flags=IGNORECASE,
    )


def format_book_num_results(book: str, book_result_count: pd.Series) -> str:
    num_results = book_result_count[book]
    return f"{book} ({num_results})"


def show_book_selector(results: List[Highlight]) -> Set[str]:
    books = pd.Series([r.book.title for r in results])
    book_result_count = books.value_counts()
    selected_books = st.multiselect(
        "Select Books",
        book_result_count.index,
        format_func=lambda x: format_book_num_results(x, book_result_count),
    )
    return set(selected_books)


def filter_results_by_book(
    results: List[Highlight], selected_books: Set[str]
) -> List[Highlight]:
    return (
        [r for r in results if r.book.title in selected_books]
        if selected_books
        else results
    )


def show_results(results):
    if results:
        st.success(f"{len(results)} highlights found.")

        selected_books = show_book_selector(results)
        selected_results = filter_results_by_book(results, selected_books)

        st.markdown("---")
        for i, result in enumerate(selected_results):
            result.text = highlight_search_query(result.text)
            show_highlight(result, i, show_book_title=True)

    elif isinstance(results, list) and len(results) == 0:
        st.warning(f"No highlights found for query: {query}")


query = st.text_input("Search String")
if query:
    results = search_highlights(query)
else:
    results = None

show_results(results)
