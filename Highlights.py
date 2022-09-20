import streamlit as st

from pages.utils.db import get_highlights, get_min_max_highlight_dates, get_categories
from pages.utils.ui import show_highlight, set_page_config, set_custom_css


set_page_config()
set_custom_css()


def reset_page():
    st.session_state.page = 1


def decrease_page():
    st.session_state.page -= 1


def increase_page():
    st.session_state.page += 1


def show_intro_text():
    st.write("# Chip's Book Highlights")
    st.write(
        "👋🏻 **Hello there, welcome to my humble Streamlit app!** I made this so I can review interesting stuff I've read from books on my Kindle. *(plus, I thought this would be a fun project to do 😄)*"
    )
    st.write(
        "✨ Whoever you are, I hope you'll find small nuggets of wisdom and inspiration from some of these quotes"
    )
    st.caption(
        "*If ever the latest highlight is from many weeks ago already, I might have not synced up my Kindle recently hehe*"
    )


def show_highlight_filters():
    st.write("---")
    st.write("## All my highlights")

    with st.expander("Apply filters"):
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
            help="I sometimes write notes to go with the highlights!",
            # on_change=reset_page(),  # buggy...
        )

        categories = get_categories()
        selected_categories = st.multiselect("Select book categories", categories)

    return date_range, with_notes_only, selected_categories


def show_pagination_buttons(num_pages: int):
    st.write(f"showing page {st.session_state.page} out of {num_pages}")
    if st.session_state.page > 1:
        col1, col2, _ = st.columns([0.2, 0.2, 0.8])
        col1.button("Previous", on_click=decrease_page)
        col2.button("Next", on_click=increase_page)
    else:
        st.button("Next", on_click=increase_page)

    st.caption(
        "*If you think the pagination isn't the best... you're right. Pagination isn't straightforward with Streamlit for now. Sorry!*"
    )


def show_highlights(date_range, with_notes_only, selected_categories):
    st.write(
        "This shows my highlights sorted by recency (with some quick filters to help me navigate)."
    )

    highlights = get_highlights(
        sort_by_recency=True,
        date_range=date_range,
        with_notes_only=with_notes_only,
        selected_categories=selected_categories,
    )

    highlight_nums = list(range(0, len(highlights) + 1))
    highlights_per_page = 10
    st.write(f"#### {len(highlights)} highlights found.")

    num_pages = int(len(highlights) / highlights_per_page) + 1

    # cheating pagination here... lol
    i = (st.session_state.page - 1) * highlights_per_page
    highlights_to_show = highlights[i : i + highlights_per_page]
    highlight_nums_to_show = highlight_nums[i : i + highlights_per_page]

    st.markdown("---")
    for i, h in zip(highlight_nums_to_show, highlights_to_show):
        show_highlight(h, i, show_book_image=True, show_book_title=True)

    show_pagination_buttons(num_pages)


if "page" not in st.session_state:
    reset_page()

show_intro_text()
filters = show_highlight_filters()
show_highlights(*filters)
