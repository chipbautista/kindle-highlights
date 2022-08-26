import time
import requests
from urllib.parse import urlencode
from typing import List

from dagster import op

from src.settings import BOOK_SEARCH_API_URL, BOOK_SEARCH_DEFAULT_PARAMS
from src.db.base import Book


@op(required_resource_keys={"db"})
def get_books_in_db(context) -> List[dict]:
    db = context.resources.db
    books = db.query(Book).filter(~Book.google_metadata.any()).all()

    context.log.info(f"Found {len(books)} in DB without metadata.")
    books = [
        {"id": book.id, "title": book.title, "author": book.author.name}
        for book in books
    ]

    return books


@op
def search_books(context, books: List[dict]) -> dict:

    search_results = {}
    for book in books:
        params = {"q": f"{book['title']}+inauthor:{book['author']}"}
        params.update(BOOK_SEARCH_DEFAULT_PARAMS)

        url = BOOK_SEARCH_API_URL.format(params=urlencode(params))
        try:
            response = requests.get(url)
            response.raise_for_status()

            search_results[book["id"]] = response.json()

        except Exception as e:
            context.log.error(f"Error for {book}: {e}")

        time.sleep(1)

    if not search_results:
        raise Exception(f"No search results found for {len(books)} books")

    return search_results


@op
def get_book_metadata(context, search_results: dict) -> List[dict]:
    book_metadata = []
    for book_id, search_result in search_results.items():
        # is the first search result always reliable?
        book = search_result["items"][0]

        required_data = [
            "title",
            "authors",
            "subtitle",
            "publishedDate",
            "description",
            "categories",
        ]

        _book_metadata = {
            "google_book_id": book["id"],
            "kindle_book_id": book_id,
            "book_cover_url": book["volumeInfo"]["imageLinks"]["thumbnail"],
        }
        _book_metadata.update(
            {k: v for (k, v) in book["volumeInfo"].items() if k in required_data}
        )
        book_metadata.append(_book_metadata)
        context.log.debug(_book_metadata)
    return book_metadata


@op
def get_book_covers_blob(context, book_metadata: List[dict]) -> List[dict]:
    for book in book_metadata:
        try:
            response = requests.get(book["book_cover_url"])
            response.raise_for_status()

            image_blob = response.content
            book["book_cover_image"] = image_blob

            context.log.debug(book)
            time.sleep(0.25)

        except Exception as e:
            context.log.error(
                f"Error: {e}. Response: {response.status_code} - {response.reason}"
            )

    return book_metadata
