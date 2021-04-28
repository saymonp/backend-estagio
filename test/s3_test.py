import pytest

from backend.services.s3 import S3
from backend.config.s3config import s3config


def test_upload_file():
    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    with open(r'C:\Users\saymo\Desktop\au.jpg', 'rb') as data:
        response = s3.upload(data, "au.jpg")

        print(response)
    assert True == True


def test_delete_file():
    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    with open(r'C:\Users\saymo\Desktop\au.jpg', 'rb') as data:
        response = s3.upload(data, "au.jpg")

    print(response)
    s3.delete(response["key"])

    print(response)
    assert True == True


def test_get_url():
    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    with open(r'C:\Users\saymo\Desktop\au.jpg', 'rb') as data:
        response = s3.upload(data, "au.jpg")

    response = s3.get_url(response["key"])

    print(response)

    assert response["file_url"] is not None
