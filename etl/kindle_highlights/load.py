import pandas as pd
from dagster import op
from sqlalchemy.orm import Session

from src.db.base import Author, Book, Highlight


@op(required_resource_keys={"db"})
def insert_highlights_to_db(context, df: pd.DataFrame):
    context.log.info(df)

    db = context.resources.db

    book_authors = df[["Book Title", "Author"]].value_counts().index.tolist()
    books = {
        book_author: get_book_object(context, db, *book_author)
        for book_author in book_authors
    }
    db.commit()

    num_new_highlights = 0
    for _, row in df.iterrows():

        book = books[(row["Book Title"], row["Author"])]
        book_highlights = set([highlight.text for highlight in book.highlights])

        if row["text"] not in book_highlights:
            highlight = Highlight(
                text=row["text"],
                note=row["Note"],
                datetime=row["datetime"],
                book_id=book.id,
            )
            db.add(highlight)
            num_new_highlights += 1

    db.commit()
    context.log.info(f"{num_new_highlights} highlights inserted to DB.")


def get_book_object(context, db: Session, book_title: str, author_name: str) -> Book:
    book = (
        db.query(Book)
        .filter((Book.title == book_title) & (Book.author.has(name=author_name)))
        .one_or_none()
    )

    if not book:
        author = Author(name=author_name)
        book = Book(title=book_title, author=author)
        context.log.info(
            f'Book: "{book_title}" - "{author_name}" will be inserted to DB.'
        )
        db.add(book)

    return book
