from time import time
from typing import List
from pathlib import Path

from dagster import op, Field
from top2vec import Top2Vec


@op(
    config_schema={
        "speed": Field(str, default_value="deep-learn"),
        "embedding_model": Field(str, default_value="universal-sentence-encoder"),
        "n_workers": Field(int, default_value=2),
        "min_word_frequency": Field(int, default_value=7),
    }
)
def train_top2vec_model(context, highlights: List[str]) -> str:
    _start_time = time()
    model = Top2Vec(
        highlights,
        speed=context.op_config["speed"],
        workers=context.op_config["n_workers"],
        embedding_model=context.op_config["embedding_model"],
        min_count=context.op_config["min_word_frequency"],
        use_embedding_model_tokenizer=True,
    )
    _end_time = time()
    _elapsed_time = _end_time - _start_time
    context.log.info(f"Topic Modeling done. ({_elapsed_time:.2f}s)")

    log_topic_previews(context, model)

    model_path = save_topic_model(context, model)
    return model_path


def log_topic_previews(context, model):
    context.log.info(f"Topic Sizes: {model.topic_sizes}")
    topic_words, _, _ = model.get_topics()

    topic_previews = [t[:10] for t in topic_words]
    for i, preview in enumerate(topic_previews):
        context.log.info(f"Topic {i}: {preview}")


def save_topic_model(context, topic_model: Top2Vec) -> str:
    Path("models").mkdir(exist_ok=True)

    model_path = "models/topic_model"
    topic_model.save(model_path)
    context.log.info(f"Topic Model saved to {model_path}")
    return model_path
