from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.base_class import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")
