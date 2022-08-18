from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    books = relationship("Highlight", back_populates="book")

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
