from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def get_db() -> Session:
    # move db value to .env
    engine = create_engine("sqlite:///highlights.db", echo=True, future=True)
    session = Session(engine)
    return session
