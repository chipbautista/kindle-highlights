import streamlit as st

from src.models.highlight import Highlight
from pages.utils.db import search_highlights
from pages.utils.ui import show_highlight

st.write("## Highlight Search")


def highlight_search_query(text: str):
    return text.replace(
        query, f"<mark style='background-color: yellow;'>{query}</mark>"
    )


def show_results(results):
    if results:
        st.success(f"{len(results)} highlights found.")
        st.markdown("---")
        for i, result in enumerate(results):
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
