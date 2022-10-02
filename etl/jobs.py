import os

import boto3
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import Session
from dagster import job, resource

from src.db.session import get_db
from etl.kindle_highlights.extract import read_clippings
from etl.kindle_highlights.transform import transform_clippings_to_dataframe
from etl.kindle_highlights.load import insert_highlights_to_db
from etl.book_metadata.extract import (
    get_books_in_db,
    search_books,
    get_book_metadata,
    get_book_covers_blob,
)
from etl.book_metadata.load import (
    insert_book_metadata_to_db,
    upload_highlights_db_to_s3,
)
from etl.topic_model.extract import get_highlights_in_db
from etl.topic_model.transform import train_top2vec_model, project_docs_to_2d
from etl.topic_model.load import upload_topic_model_to_s3


@resource
def get_s3_bucket(init_context) -> Session:
    try:
        load_dotenv(find_dotenv())
        s3 = boto3.resource(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID_WRITE"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY_WRITE"],
        )
        bucket = s3.Bucket(os.environ["S3_BUCKET"])
        yield bucket
    finally:
        pass


@resource
def get_db_session(init_context) -> Session:
    try:
        db = get_db()
        yield db
    finally:
        db.close()


@job(resource_defs={"db": get_db_session})
def import_kindle_clippings():
    clippings_text = read_clippings()
    highlights_df = transform_clippings_to_dataframe(clippings_text)
    insert_highlights_to_db(highlights_df)


@job(resource_defs={"db": get_db_session, "s3_bucket": get_s3_bucket})
def get_google_books_metadata():
    books_in_db = get_books_in_db()
    books_search_results = search_books(books_in_db)
    book_metadata = get_book_metadata(books_search_results)
    book_metadata = get_book_covers_blob(book_metadata)

    _ = insert_book_metadata_to_db(book_metadata)

    upload_highlights_db_to_s3(_)


@job(resource_defs={"db": get_db_session, "s3_bucket": get_s3_bucket})
def run_topic_modeling():
    highlights = get_highlights_in_db()
    model_path = train_top2vec_model(highlights)
    vectors_path = project_docs_to_2d(model_path)

    # model_path = save_topic_model(model)
    # vectors_path = save_tsne_vectors(tsne_vectors)

    upload_topic_model_to_s3(model_path, vectors_path)
