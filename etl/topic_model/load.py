from pathlib import Path

import pickle
from dagster import op, Field


def save_topic_model(context, topic_model) -> str:
    Path("models").mkdir(exist_ok=True)

    model_path = "models/topic_model"
    topic_model.save(model_path)
    context.log.info(f"Topic Model saved to {model_path}")
    return model_path


def save_tsne_vectors(context, tsne_vectors):
    path = "models/tsne_vectors.pkl"
    with open(path, "wb") as f:
        pickle.dump(tsne_vectors, f)
    context.log.info(f"TSNE vectors {tsne_vectors.shape} saved to {path}")
    return path


@op(
    config_schema={"upload_to_s3": Field(bool, default_value=False)},
    required_resource_keys={"s3_bucket"},
)
def upload_topic_model_to_s3(context, model_path: str, vectors_path: str):
    if not context.op_config["upload_to_s3"]:
        context.log.info(f"Skipping S3 upload")
        return

    s3_bucket = context.resources.s3_bucket
    model_filename = model_path.split("/")[-1]
    vectors_filename = vectors_path.split("/")[-1]

    try:
        s3_bucket.upload_file(model_path, model_filename)
        s3_bucket.upload_file(vectors_path, vectors_filename)
    except Exception as e:
        context.log.error(e)
        raise

    context.log.info(f"Topic model saved to s3://{s3_bucket._name}/{model_filename}.")
    context.log.info(
        f"TSNE vectors saved to s3://{s3_bucket._name}/{vectors_filename}."
    )
