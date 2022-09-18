from typing import List

import streamlit as st
import pandas as pd
import plotly.express as px
from numpy import ndarray
from sklearn.manifold import TSNE

from pages.utils.model import get_topic_model
from pages.utils.db import get_highlights
from pages.utils.ui import show_analysis_note, show_highlight

st.set_page_config(layout="wide")


def get_topics_df(model) -> pd.DataFrame:
    (
        doc_topics,
        doc_topic_scores,
        _,
        _,
    ) = model.get_documents_topics(model.document_ids)
    topic_names = get_topic_names(model)

    df = pd.DataFrame(
        zip(
            doc_topics,
            doc_topic_scores,
        ),
        columns=["topic", "topic_score"],
    )

    df["topic_name"] = df["topic"].apply(lambda x: topic_names[x])
    df["text"] = model.documents

    df["text_wrap"] = df["text"].str.wrap(80).str.replace("\n", "<br>")

    # remove negative score
    df["topic_score_min0"] = df["topic_score"].apply(lambda x: x if x >= 0 else 0)
    # simplify for display in plot
    df["topic_score_disp"] = df["topic_score"].round(1).astype(str)

    docs_2d = project_docs_to_2d(model.document_vectors)
    df["tsne_1"] = docs_2d[:, 0]
    df["tsne_2"] = docs_2d[:, 1]

    df = join_model_output_with_highlights_db(df)
    return df


def join_model_output_with_highlights_db(topics_df):
    highlights = get_highlights()
    highlights_ = pd.Series(highlights, name="highlight_db_obj")
    highlights_.index = [h.text for h in highlights]

    topics_df = topics_df.merge(highlights_, left_on="text", right_index=True)

    return topics_df


def get_topic_names(model, top_n: int = 5) -> List[str]:
    topic_words, _, _ = model.get_topics()
    topic_names = [", ".join(words[:top_n]) for words in topic_words]
    return topic_names


@st.cache
def project_docs_to_2d(doc_vectors: ndarray) -> ndarray:
    with st.spinner("Projecting documents to 2 dimensions..."):
        tsne = TSNE(init="pca", learning_rate="auto", perplexity=30, random_state=123)
        return tsne.fit_transform(doc_vectors)


def show_tsne_plot(df):
    st.write("### 🗺 All my highlights in Euclidean space")
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
                addtl_metadata=f"| Topic Score: {score}",
            )


st.write("## Highlights by Topic")
st.write(
    "I thought it would be fun to have a model automatically categorize my highlights for me, so I trained a simple Top2Vec model! This page shows the visualizations from the model output."
)
show_analysis_note()

model = get_topic_model()
topics_df = get_topics_df(model)

show_tsne_plot(topics_df)
show_top_highlights_per_topic(topics_df)
