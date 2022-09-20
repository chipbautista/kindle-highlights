import streamlit as st

from src.db.base import Highlight


def set_custom_font():

    with open("pages/utils/Aboreto-base64.txt", "r") as f:
        aboreto_base64 = f.read()

    streamlit_style = f"""
    <style>
    
    @font-face {{
        font-family: 'Aboreto-Regular';
        src: url(data:font/truetype;charset=utf-8;base64,{aboreto_base64}) format('truetype');  
    }}

    h1, h2, h3, h4, h5, div[data-testid="stSidebarNav"] {{
        font-family: 'Aboreto-Regular', serif;
    }}
    </style>
    """
    st.markdown(streamlit_style, unsafe_allow_html=True)


def format_datetime(x: str) -> str:
    return x.strftime("%B %d, %Y %I:%M %p")


def show_highlight(
    highlight: Highlight,
    i: int,
    show_book_title: bool = False,
    show_book_image: bool = False,
    addtl_metadata: str = "",
):
    def show_highlight_and_metadata():
        st.markdown(f"#### #{i + 1}")
        st.caption(f"{datetime_formatted}{addtl_metadata}")
        st.markdown(f"{highlight.text}", unsafe_allow_html=True)
        if highlight.note:
            st.info(f"""🙋🏻‍♀️ **Chip's Note**: *{highlight.note}*""")

    def show_book_info():
        if show_book_image and highlight.book.google_metadata:
            st.image(highlight.book.google_metadata[0].cover_image)

        st.markdown(f"**{highlight.book.title}** ({highlight.book.author.name})")

    datetime_formatted = format_datetime(highlight.datetime)
    addtl_metadata = f" | {addtl_metadata}" if addtl_metadata else ""

    if not show_book_title:  # single-column text
        show_highlight_and_metadata()

    else:
        book_col, text_col = st.columns([0.2, 0.8])
        with text_col:
            show_highlight_and_metadata()
        with book_col:
            show_book_info()

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
