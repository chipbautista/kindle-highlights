from typing import List

import streamlit as st
import pandas as pd
import plotly.express as px
from numpy import ndarray
from sklearn.manifold import TSNE

from pages.utils.model import get_topic_model
from pages.utils.ui import show_analysis_note

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
    return df


def get_topic_names(model, top_n: int = 5) -> List[str]:
    topic_words, _, _ = model.get_topics()
    topic_names = [", ".join(words[:top_n]) for words in topic_words]
    return topic_names


@st.cache
def project_docs_to_2d(doc_vectors: ndarray) -> ndarray:
    with st.spinner("Projecting documents to 2 dimensions..."):
        tsne = TSNE(init="pca", learning_rate="auto", perplexity=30, random_state=123)
        return tsne.fit_transform(doc_vectors)


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


st.write("## Highlights by Topic")
st.write(
    "I thought it would be fun to have a model automatically categorize my highlights for me, so I trained a simple Top2Vec model! This page shows the visualizations from the model output."
)
show_analysis_note()

model = get_topic_model()
topics_df = get_topics_df(model)

st.write("### All my highlights in Euclidean space")
plot_2d_docs(topics_df)
