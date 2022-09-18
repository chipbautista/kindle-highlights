from typing import List

from dagster import op

from src.db.base import Highlight


@op(required_resource_keys={"db"})
def get_highlights_in_db(context) -> List[str]:
    db = context.resources.db
    highlights = [h.text for h in db.query(Highlight).all()]
    context.log.info(f"Found {len(highlights)} from db.")
    return highlights
