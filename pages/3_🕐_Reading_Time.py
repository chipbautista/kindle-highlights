import streamlit as st
import pandas as pd
from plotly_calplot import calplot

from src.db.base import Highlight
from pages.utils.db import get_app_db


# @st.cache
def get_highlight_datetimes():
    db = get_app_db()
    all_datetime = db.query(Highlight.datetime).all()
    df = pd.DataFrame(all_datetime)
    return df


def get_highlight_count_per_date(dates: pd.Series):
    counts_df = (
        dates.value_counts()
        .reset_index()
        .rename(columns={"index": "date", "datetime": "count"})
    )

    counts_df["date"] = pd.to_datetime(counts_df["date"])
    return counts_df


def show_calendar_heatmap(df):
    counts_df = get_highlight_count_per_date(df["datetime"].dt.date)

    fig = calplot(counts_df, x="date", y="count")

    st.write("### How much have I read the past year or so?")
    st.plotly_chart(fig)


# def preprocess_datetime_df(df):
#     df['month'] = df.datetime.dt.month_name()
st.write("## Reading Time Analysis")
st.write("Quick visualizations of my reading behavior")
st.write("*I guess the number of highlights can act as a proxy...*")

df = get_highlight_datetimes()

show_calendar_heatmap(df)
