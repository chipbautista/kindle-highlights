import pickle
import _thread
import weakref

from typing import List, Tuple, Dict

import streamlit as st
import pandas as pd
from top2vec import Top2Vec

from src.models.highlight import Highlight
from pages.utils.s3 import download_from_s3
from pages.utils.db import get_highlights_series

ENV = st.secrets.get("ENV", "dev")


@st.cache(
    allow_output_mutation=True,
    hash_funcs={_thread.RLock: lambda _: None, weakref.ReferenceType: lambda _: None},
)
def get_topic_model() -> Top2Vec:
    with st.spinner("Loading topic model..."):
        topic_model_path = st.secrets.get("TOPIC_MODEL")
        if ENV != "dev":
            download_from_s3(topic_model_path)

        model = Top2Vec.load(topic_model_path)
        print(f"Topic model loaded from {topic_model_path}")

    return model


@st.cache(
    allow_output_mutation=True,
    hash_funcs={_thread.RLock: lambda _: None, weakref.ReferenceType: lambda _: None},
)
def get_tsne_vectors():
    with st.spinner("Loading 2D vectors..."):
        vectors_path = st.secrets.get("TSNE_VECTORS")
        if ENV != "dev":
            download_from_s3(vectors_path)

        with open(vectors_path, "rb") as f:
            vectors = pickle.load(f)
        print(f"TSNE vectors loaded from {vectors_path}")
        return vectors


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

    df = join_model_output_with_highlights_db(df)
    return df


def join_model_output_with_highlights_db(topics_df):
    highlights = get_highlights_series()
    topics_df = topics_df.merge(highlights, left_on="text", right_index=True)

    return topics_df


def get_topic_names(model, top_n: int = 5) -> List[str]:
    topic_words, _, _ = model.get_topics()
    topic_names = [", ".join(words[:top_n]) for words in topic_words]
    return topic_names


def search_semantic(query) -> Tuple[List[Highlight], Dict]:
    model = get_topic_model()
    results, scores, _ = model.query_documents(query, num_docs=10)
    scores = dict(zip(results, scores))

    highlights = get_highlights_series()
    results = highlights.loc[results].values.tolist()
    return results, scores
