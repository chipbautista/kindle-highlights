import streamlit as st

from src.models.book import Book
from pages.utils import ui, db


def format_book_title(book: Book):
    return f"{book.title} ({book.author.name}) - ({len(book.highlights)})"


def book_selector(books, book_index) -> int:
    selected_book_index = st.selectbox(
        "Select Book",
        [""] + book_index,
        format_func=lambda x: format_book_title(books[x]) if x != "" else "",
    )
    st.markdown("---")
    return selected_book_index


def show_book_metadata(book):
    if book.google_metadata:
        metadata = book.google_metadata[0]
        img_col, metadata_col = st.columns([0.2, 0.8])
        with img_col:
            st.image(metadata.cover_image)
        with metadata_col:
            st.markdown(f"### {metadata.title}")
            if metadata.subtitle:
                st.markdown(f"#### *{metadata.subtitle}*")
            st.markdown(f"by {book.author.name}")

            st.caption(f"Published {metadata.published_date}")
            st.caption(f"Categories: {metadata.categories}")

        with st.expander("Show synopsis"):
            st.markdown(metadata.description)


st.write("## Book Highlights")
st.write("This page shows all the highlights per book. Select one to get started!")

books = db.get_books()
book_index = list(range(len(books)))
selected_book_index = book_selector(books, book_index)

if selected_book_index != "":
    book = books[selected_book_index]
    highlights = book.highlights
    highlights_w_notes = [h for h in highlights if h.note]

    show_book_metadata(book)
    col1, col2 = st.columns(2)
    col1.write(
        f"{len(book.highlights)} highlights found ({len(highlights_w_notes)} with notes)"
    )
    with_notes_only = col2.checkbox(
        "Show highlights with notes only",
        False,
        help="I sometimes write notes to go with the highlights!",
    )
    st.markdown("---")

    highlights_to_display = highlights if not with_notes_only else highlights_w_notes
    for i, highlight in enumerate(highlights_to_display):
        ui.show_highlight(highlight, i)
