import streamlit as st

from pages.utils import ui, db


def book_selector(books, book_index) -> int:
    selected_book_index = st.selectbox(
        "Select Book",
        book_index,
        format_func=lambda x: ui.format_book_title(books[x]),
    )
    return selected_book_index


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


st.write("## Book Highlights")

books = db.get_books()
book_index = list(range(len(books)))
selected_book_index = book_selector(books, book_index)

book = books[selected_book_index]
highlights = book.highlights
highlights_w_notes = [h for h in highlights if h.note]

show_book_metadata(book)
st.write(
    f"{len(book.highlights)} highlights found ({len(highlights_w_notes)} with notes)"
)
with_notes_only = st.checkbox("Show highlights with notes only", False)
st.markdown("---")

highlights_to_display = highlights if not with_notes_only else highlights_w_notes
for i, highlight in enumerate(highlights_to_display):
    ui.show_highlight(highlight, i)
