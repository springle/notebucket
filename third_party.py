import os
import requests

from google.cloud import storage

BUCKET_NAME = "notebucket"


def download_blob(blob_name: str) -> str:
    bucket = storage.Client().bucket(BUCKET_NAME)
    return storage.Blob(blob_name, bucket).download_as_string().decode("utf-8")


def upload_blob(blob_name: str, data: bytes):
    assert len(data) <= 1e6
    bucket = storage.Client().bucket(BUCKET_NAME)
    storage.Blob(blob_name, bucket).upload_from_string(data)


def is_valid_token(token: str) -> bool:
    return requests.post(
        url="https://www.google.com/recaptcha/api/siteverify",
        params={
            "secret": os.getenv("RECAPTCHA_SECRET"),
            "response": token,
        }
    ).json()["success"]
