import boto3
import streamlit as st


def download_from_s3(s3_file: str) -> str:

    # if file == "db":
    #     s3_file = st.secrets["aws"]["DB_FILE"]
    # elif file == "topic_model":
    #     s3_file = st.secrets["TOPIC_MODEL"]

    s3 = boto3.client(
        "s3",
        aws_access_key_id=st.secrets["aws"]["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["aws"]["AWS_SECRET_ACCESS_KEY"],
    )
    s3.download_file(st.secrets["aws"]["BUCKET"], s3_file, s3_file)
    print("Database downloaded from S3.")
    return s3_file
