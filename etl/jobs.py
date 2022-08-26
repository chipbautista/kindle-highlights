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

from etl.book_metadata.load import insert_book_metadata_to_db


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


@job(resource_defs={"db": get_db_session})
def get_google_books_metadata():
    books_in_db = get_books_in_db()
    books_search_results = search_books(books_in_db)
    book_metadata = get_book_metadata(books_search_results)
    book_metadata = get_book_covers_blob(book_metadata)

    insert_book_metadata_to_db(book_metadata)
