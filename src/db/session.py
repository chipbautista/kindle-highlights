from sqlalchemy import create_engine

# move db value to .env
engine = create_engine("sqlite:///highlights.db", echo=True, future=True)
