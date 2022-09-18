import streamlit as st

from pages.utils.db import get_highlights, get_min_max_highlight_dates
from pages.utils.ui import show_highlight

st.set_page_config(
    page_title="Chip's Book Highlights",
    page_icon="👋",
)


def show_highlight_filters():
    st.write("---")
    st.write("## All my highlights")

    min_date, max_date = get_min_max_highlight_dates()
    date_range = st.date_input(
        "Date Range (Optional)",
        value=[],
        min_value=min_date,
        max_value=max_date,
        help="You may also select a minimum date",
    )
    with_notes_only = st.checkbox(
        "Show highlights with notes only",
        False,
        help="I sometimes annotate the highlights!",
    )
    st.markdown("---")
    return date_range, with_notes_only


def show_highlights(date_range, with_notes_only):
    if not date_range:
        highlights = get_highlights(
            sort_by_recency=True, with_notes_only=with_notes_only
        )
    else:
        highlights = get_highlights(
            sort_by_recency=True, date_range=date_range, with_notes_only=with_notes_only
        )

    for i, h in enumerate(highlights[:10]):
        show_highlight(h, i, show_book_image=True, show_book_title=True)


st.write("# Chip's Book Highlights")
st.write(
    "👋🏻 **Hello there, welcome to my humble Streamlit app!** I made this so I can review interesting stuff I've read from books on my Kindle. *(plus, I thought this would be a fun project to do 😄)*"
)
st.write(
    "This page shows my recent highlights, but I also added some quick filters for navigation."
)
st.caption(
    "*If ever the latest highlight is from many weeks ago already, I might have not synced up my Kindle recently*"
)
date_range, with_notes_only = show_highlight_filters()
show_highlights(date_range, with_notes_only)
