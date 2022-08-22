from src.db.base import Book


def format_book_title(book: Book):
    return f"{book.title} ({book.author.name})"


def format_datetime(x: str) -> str:
    return x.strftime("%B %d, %Y %I:%M %p")
