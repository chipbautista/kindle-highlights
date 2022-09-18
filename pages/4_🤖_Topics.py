import streamlit as st
import plotly.express as px
from numpy import ndarray

from pages.utils.model import get_topics_df, get_topic_model, get_tsne_vectors
from pages.utils.ui import show_analysis_note, show_highlight

st.set_page_config(layout="wide")


def add_tsne_vectors_to_df(df):
    docs_2d = get_tsne_vectors()

    df["tsne_1"] = docs_2d[:, 0]
    df["tsne_2"] = docs_2d[:, 1]
    return df


def show_tsne_plot(df):
    st.write("### 🗺 All my highlights in Euclidean space")

    ### Removing this for now -- runs too slow unless cached tsne works perfectly
    max_score = df["topic_score_min0"].max()
    min_topic_score = st.slider(
        "Set minimum topic score",
        0.00,
        max_score,
        value=0.10,
        step=0.1,
        format="%.2f",
    )

    filtered_df = df[df["topic_score_min0"] >= min_topic_score]
    st.write(f"{len(filtered_df)} out of {len(df)} highlights displayed.")
    plot_2d_docs(filtered_df)


def plot_2d_docs(df):
    with st.spinner("Generating plot..."):
        fig = px.scatter(
            df,
            x="tsne_1",
            y="tsne_2",
            color="topic_name",
            size="topic_score_min0",
            hover_name="text_wrap",
            hover_data={
                "tsne_1": False,
                "tsne_2": False,
                "topic_score_min0": False,
                "topic_score_disp": True,
            },
            labels={"topic_name": "Topic", "topic_score_disp": "Topic Score"},
            height=600,
            width=900,
        )
    fig.update_layout(
        title="Highlights Projection",
        hoverlabel=dict(font_color="white"),
        legend=dict(yanchor="bottom", y=-0.5, xanchor="left", x=0.00),
        xaxis=dict(title=None, showticklabels=False, showgrid=False),
        yaxis=dict(title=None, showticklabels=False, showgrid=False),
        plot_bgcolor="rgb(250,250,250)",
        margin=dict(l=20, r=20, b=20),
    )
    st.plotly_chart(fig)

    with st.expander("💡 You can interact with the plot!"):
        st.info(
            """
            Click on the legend to filter by topic (double-click to select one and deselect everything else).
            
            The size of the dot indicates the document score. The bigger it is, the more certain that it belongs to the topic :)
            """
        )
        st.write()


def show_top_highlights_per_topic(df):
    st.write("---")
    st.write("### 👑 Top highlights per topic")

    topic_col, n_col = st.columns([0.8, 0.2])
    with topic_col:
        topic_names = df["topic_name"].unique()
        selected_topic = st.selectbox("Select topic", topic_names)
    with n_col:
        top_n = st.number_input(
            "n highlights", min_value=1, max_value=20, value=3, step=1
        )

    if selected_topic:
        topic_df = (
            df[df["topic_name"] == selected_topic]
            .sort_values("topic_score", ascending=False)
            .reset_index()
        )

        for i, row in topic_df[:top_n].iterrows():
            highlight = row["highlight_db_obj"]
            score = row["topic_score_disp"]
            show_highlight(
                highlight,
                i,
                show_book_title=True,
                addtl_metadata=f" | Topic Score: {score}",
            )


st.write("## Highlights by Topic")
st.write(
    "I thought it would be fun to have a model automatically categorize my highlights for me, so I trained a simple Top2Vec model! This page shows the visualizations from the model output."
)
show_analysis_note()

model = get_topic_model()
topics_df = get_topics_df(model)
topics_df = add_tsne_vectors_to_df(topics_df)

show_tsne_plot(topics_df)
show_top_highlights_per_topic(topics_df)
