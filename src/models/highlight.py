from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship
from src.db.base import Base


class Highlight(Base):
    __tablename__ = "highlights"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    datetime = Column(DATETIME, nullable=False)

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="books")