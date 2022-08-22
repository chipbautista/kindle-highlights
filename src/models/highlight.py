from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import relationship
from src.db.base_class import Base


class Highlight(Base):
    __tablename__ = "highlights"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    note = Column(String)
    datetime = Column(DATETIME, nullable=False)

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="highlights")
