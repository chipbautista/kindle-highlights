from typing import List

from dagster import op
from src.db.base import Metadata


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
