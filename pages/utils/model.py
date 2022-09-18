import streamlit as st
from top2vec import Top2Vec

from .s3 import download_from_s3

ENV = st.secrets.get("ENV", "dev")
TOPIC_MODEL_PATH = st.secrets.get("TOPIC_MODEL")


def get_topic_model() -> Top2Vec:
    with st.spinner("Loading topic model..."):
        topic_model_path = (
            TOPIC_MODEL_PATH
            if ENV == "dev"
            else download_from_s3("topic_model", st.secrets["aws"])
        )

        model = Top2Vec.load(topic_model_path)
        print(f"Topic model loaded from {topic_model_path}")

    return model
