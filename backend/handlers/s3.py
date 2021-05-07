import json

from ..services.s3 import S3
from ..config.s3config import s3config
from ..util import lambda_method, lambda_method_custom, auth, required
from ..env import DELETEPRODUCT
from ..errors import AppError

# pylint: disable=no-value-for-parameter


@lambda_method
def upload_file(event, context, **kwargs):

    body = json.loads(event["body"])

    data = required(body["data"], str)
    file_name = required(body["file_name"], str)
    path = required(body["path"], str)

    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    upload_image = s3.upload(data, file_name, path)

    return upload_image


@auth(DELETEPRODUCT)
@lambda_method_custom
def delete_file(event, context, **kwargs):

    body = event["body"]

    key = required(body["key"], str)

    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    deleted_file = s3.delete(body["key"])

    return deleted_file
