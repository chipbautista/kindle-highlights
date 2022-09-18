import streamlit as st

from src.db.base import Highlight


def format_datetime(x: str) -> str:
    return x.strftime("%B %d, %Y %I:%M %p")


def show_highlight(
    highlight: Highlight,
    i: int,
    show_book_title: bool = False,
    addtl_metadata: str = "",
):
    datetime_formatted = format_datetime(highlight.datetime)
    st.markdown(f"##### #{i + 1}")

    st.markdown(f"{highlight.text}", unsafe_allow_html=True)
    if show_book_title:
        st.markdown(f"*{highlight.book.title} ({highlight.book.author.name})*")
    if highlight.note:
        st.markdown(f"*{highlight.note}*")

    st.markdown(
        f'<font color="grey">*{datetime_formatted}{addtl_metadata}*</font>',
        unsafe_allow_html=True,
    )
    st.markdown("---")


def show_analysis_note():
    with st.expander("🙋🏻‍♀️ A quick note on analysis"):
        st.write(
            """
            *I am deliberately not writing any analysis on the viz presented in this page because
            these charts are generated dynamically -- they're supposed to change everytime I update my highlights.
            In that sense it's more of a "dashboard" for me.* 😁
            """
        )
