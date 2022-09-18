from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly_calplot import calplot

from src.db.base import Highlight
from pages.utils.db import get_app_db
from pages.utils.ui import show_analysis_note


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

    st.write("---")
    st.write("### How much have I read the past year or so?")
    st.plotly_chart(fig)


def to_ampm(x):
    if x == 0:
        return "12 AM"
    if 0 < x < 12:
        return f"{x} AM"
    if x == 12:
        return "12 PM"
    else:
        return f"{x - 12} PM"


def get_highlight_stats_per_day_hr(df):
    df["hour"] = df.datetime.dt.hour

    hrs = list(range(0, 24))
    hrs_shifted = [int(x) for x in np.roll(hrs, 7)]  # make 7AM to be the 0 in the chart
    shift_mapping = dict(zip(hrs, hrs_shifted))

    hrs_ampm = [to_ampm(hr) for hr in hrs]
    ampm_mapping = dict(zip(hrs, hrs_ampm))
    df["hour_shifted"] = df["hour"].apply(lambda x: shift_mapping[x])
    df["hour_ampm"] = df["hour"].apply(lambda x: ampm_mapping[x])

    df["day of week"] = df.datetime.dt.dayofweek
    df["_c"] = 1
    df["days_since"] = (datetime.now() - df.datetime).dt.days
    agg_df = (
        df.groupby(["day of week", "hour_shifted"])
        .agg({"_c": "sum", "days_since": "mean"})
        .reset_index()
        .rename(columns={"_c": "highlights", "days_since": "ave. recency (days)"})
    )
    return agg_df, hrs_shifted, hrs_ampm


def show_time_scatterplot(df):

    agg_df, hrs_shifted, hrs_ampm = get_highlight_stats_per_day_hr(df)
    fig = px.scatter(
        agg_df,
        x="day of week",
        y="hour_shifted",
        size="highlights",
        color="ave. recency (days)",
    )
    yaxis_format = {
        "title": "",
        "tickmode": "array",
        "tickvals": hrs_shifted,
        "ticktext": hrs_ampm,
    }
    xaxis_format = {
        "title": "",
        "tickmode": "array",
        "tickvals": [0, 1, 2, 3, 4, 5, 6],
        "ticktext": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
    }
    fig.update_layout(yaxis=yaxis_format, xaxis=xaxis_format)

    st.write("---")
    st.write("### What time of the day do I read?")
    st.plotly_chart(fig)


st.write("## Reading Time Analysis")
st.write(
    "Quick visualizations of my reading behavior (with highlight activity as a **proxy**)"
)
st.write(
    "\nI admit, I'm not as big of a reader as I want to be. I'm hoping seeing my '''reading activity''' presented like this will motivate me to read more :)"
)
st.write(
    "*Of course, no highlights does not always mean I'm not reading. Maybe the book I'm reading just doesn't have highlight-worthy passages lol*"
)

show_analysis_note()


df = get_highlight_datetimes()

show_calendar_heatmap(df)

show_time_scatterplot(df)
