import streamlit as st

import ui
import db_utils

st.title("My Kindle Highlights")

books = db_utils.get_books()
book_index = list(range(len(books)))
selected_book_index = ui.book_selector(books, book_index)

book = books[selected_book_index]
highlights = book.highlights
highlights_w_notes = [h for h in highlights if h.note]

ui.show_book_metadata(book)
st.write(
    f"{len(book.highlights)} highlights found ({len(highlights_w_notes)} with notes)"
)
with_notes_only = st.checkbox("Show highlights with notes only", False)
st.markdown("---")

highlights_to_display = highlights if not with_notes_only else highlights_w_notes
ui.show_highlights(highlights_to_display)
