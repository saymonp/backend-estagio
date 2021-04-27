import pytest

from backend.services.s3 import S3
from backend.config import s3config


def test_user_registration():
    s3 = S3(s3config.bucket_name, s3config.limits_file_size)

    

    assert response == {"msg": "Verification email sent"}