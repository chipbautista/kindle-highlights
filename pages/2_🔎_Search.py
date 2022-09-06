import streamlit as st

from pages.utils.db import search_highlights
from pages.utils.ui import show_highlight

st.write("## Highlight Search")

query = st.text_input("Search String")
results = search_highlights(query)

if results:
    st.markdown("---")
    for i, result in enumerate(results):
        show_highlight(result, i, show_book_title=True)
