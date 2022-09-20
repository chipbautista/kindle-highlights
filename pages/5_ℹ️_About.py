import streamlit as st

from pages.utils.ui import set_page_config, set_custom_css

set_page_config()
set_custom_css()

st.write("## About")
st.write(
    "This app is part of my fun mini project that takes my kindle highlights from end-to-end: from Kindle's highlights file, to ETL pipelines, and then to this UI. If you're curious enough, [my code is open source](https://github.com/chipbautista/kindle-highlights)! "
)
st.write(
    "This app is made with [Streamlit](https://streamlit.io), and is also hosted with Streamlit -- they're kind enough to offer free and *suuuuper* convenient hosting (one-click deploy, CI/CD, etc. -- I'm a fan!) But that also means this app is provided limited resources, so please excuse the slow loading times 😄"
)

st.write(
    "📩 If you have feedback or book suggestions, I can be reached at chippybautista@gmail.com."
)
