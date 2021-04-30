import json

from ..services.s3 import S3
from ..config.s3config import s3config
from ..util import lambda_method, lambda_method_custom, auth
from ..env import DELETEPRODUCT

# pylint: disable=no-value-for-parameter


@lambda_method
def upload_file(event, context, **kwargs):
    body = json.loads(event["body"])
       
    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)
    
    upload_image = s3.upload(body["data"], body["fileName"], body["path"])

    return upload_image


@auth(DELETEPRODUCT)
@lambda_method_custom
def delete_file(event, context, **kwargs):
    body = event["body"]

    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    deleted_file = s3.delete(body["key"])

    return deleted_file

