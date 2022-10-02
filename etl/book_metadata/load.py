from typing import List

from dagster import op, Field
from src.db.base import Metadata

from dotenv import dotenv_values


@op(required_resource_keys={"db"})
def insert_book_metadata_to_db(context, book_metadata: List[dict]):
    db = context.resources.db

    for metadata in book_metadata:
        metadata_obj = Metadata(
            google_id=metadata["google_book_id"],
            book_id=metadata["kindle_book_id"],
            title=metadata["title"],
            subtitle=metadata.get("subtitle"),
            authors=", ".join(metadata.get("authors", [])),
            categories=", ".join(metadata.get("categories", [])),
            description=metadata.get("description"),
            published_date=metadata.get("publishedDate"),
            cover_image=metadata["book_cover_image"],
        )
        db.merge(metadata_obj)

    db.commit()
    context.log.info(f"{len(book_metadata)} book metadata inserted to DB.")
    return 1


@op(
    config_schema={"upload_to_s3": Field(bool, default_value=False)},
    required_resource_keys={"s3_bucket"},
)
def upload_highlights_db_to_s3(context, _):
    if not context.op_config["upload_to_s3"]:
        context.log.info(f"Skipping S3 upload")
        return

    env = dotenv_values()
    db_filename = env.get("SQLITE_DB").split("/")[-1]

    s3_bucket = context.resources.s3_bucket
    # db_filename = model_path.split("/")[-1]

    try:
        s3_bucket.upload_file(db_filename, db_filename)
    except Exception as e:
        context.log.error(e)
        raise

    context.log.info(f"Highlights DB saved to s3://{s3_bucket._name}/{db_filename}.")
