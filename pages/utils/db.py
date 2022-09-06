from typing import List

import streamlit as st

from src.db.base import Book, Highlight
from src.db.session import get_db

import boto3
from dotenv import dotenv_values

env = dotenv_values()
ENV = st.secrets.get("ENV", "dev")


@st.cache
def get_db_from_s3(aws_secrets: dict):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=aws_secrets["AWS_SECRET_ACCESS_KEY"],
    )
    s3.download_file(
        aws_secrets["BUCKET"], aws_secrets["DB_FILE"], aws_secrets["DB_FILE"]
    )
    print("Database downloaded from S3.")
    return aws_secrets["DB_FILE"]


def get_app_db():
    if ENV == "dev":
        db = get_db()
    else:
        db_file = get_db_from_s3(st.secrets["aws"])
        db = get_db(db_url=f"sqlite:///{db_file}")
    return db


# @st.cache -- cached outputs will be detached objects from DB
def get_books():
    db = get_app_db()
    books = db.query(Book).all()
    return books


def search_highlights(query: str) -> List[Highlight]:
    if query:
        db = get_app_db()
        result = db.query(Highlight).filter(Highlight.text.contains(query)).all()
        # to-do: pagination
        return result[:50]
    return []
