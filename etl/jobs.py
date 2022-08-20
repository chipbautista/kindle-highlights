from sqlalchemy.orm import Session
from dagster import job, resource

from src.db.session import get_db
from etl.etl import extract, transform, load


@resource
def get_db_session(init_context) -> Session:
    try:
        db = get_db()
        yield db
    finally:
        db.close()


@job(resource_defs={"db": get_db_session})
def import_kindle_clippings():
    clippings_text = extract.read_clippings()
    highlights_df = transform.transform_clippings_to_dataframe(clippings_text)
    load.insert_to_db(highlights_df)
