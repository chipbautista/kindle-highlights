from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dotenv import dotenv_values

env = dotenv_values()
local_sqlite_db = env.get("SQLITE_DB")


def get_db(db_url: str = local_sqlite_db) -> Session:
    # move db value to .env
    engine = create_engine(db_url, echo=True, future=True)
    session = Session(engine)
    return session
