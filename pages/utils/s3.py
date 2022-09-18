import boto3
import streamlit as st


@st.cache
def download_from_s3(file: str, aws_secrets: dict) -> str:

    if file == "db":
        s3_file = aws_secrets["DB_FILE"]
    elif file == "topic_model":
        s3_file = aws_secrets["TOPIC_MODEL"]

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=aws_secrets["AWS_SECRET_ACCESS_KEY"],
    )
    s3.download_file(aws_secrets["BUCKET"], s3_file, s3_file)
    print("Database downloaded from S3.")
    return s3_file
