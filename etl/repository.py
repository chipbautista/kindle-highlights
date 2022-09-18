from dagster import repository

from etl.jobs import (
    import_kindle_clippings,
    get_google_books_metadata,
    run_topic_modeling,
)


@repository
def etl():
    return [import_kindle_clippings, get_google_books_metadata, run_topic_modeling]
