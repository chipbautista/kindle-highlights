from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.sqlite import DATETIME, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.base_class import Base


class Metadata(Base):
    __tablename__ = "metadata"

    google_id = Column(String, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    subtitle = Column(String)

    # keeping it simple, if there are multiple authors then save as a list
    authors = Column(String)
    description = Column(String)
    published_date = Column(String)
    categories = Column(String)
    cover_image = Column(BLOB)

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="google_metadata")

    updated_at = Column(
        DATETIME, server_default=func.now(), onupdate=func.current_timestamp()
    )
