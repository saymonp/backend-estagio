import json

from ..services.s3 import S3
from ..config.s3config import s3config

from ..util import lambda_method, lambda_method_custom, auth
from ..errors import AppError
from ..env import DELETEUSER, UPDATEUSER, CREATEUSER

import bcrypt
from base64 import b64decode

# pylint: disable=no-value-for-parameter


@lambda_method
def upload_image_project(event, context, **kwargs):
    body = event["body"]
    pp = event['pathParameters']
   
    imgdata = b64decode(body)
    
    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)
    
    upload_image = s3.upload(imgdata, pp["fileName"], "projects/images/")

    return {"img": upload_image, "event": event}

@lambda_method
def upload_image_product(event, context, **kwargs):
    body = event["body"]
    pp = event['pathParameters']
    file = b64decode(body)

    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    upload_image = s3.upload(file, pp["fileName"], "products/images/")

    return upload_image

@lambda_method
def upload_3dmodel_project(event, context, **kwargs):
    body = event["body"]
    pp = event['pathParameters']
    file = b64decode(body)

    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    upload_file = s3.upload(file, pp["fileName"], "projects/images/",)

    return upload_file

@lambda_method
def upload_3dmodel_product(event, context, **kwargs):
    body = event["body"]
    pp = event['pathParameters']
    file = b64decode(body)

    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    upload_file = s3.upload(file, pp["fileName"], "projects/images/")

    return upload_file

@lambda_method
def delete_file(event, context, **kwargs):
    pp = event['pathParameters']

    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    deleted_file = s3.delete(pp["key"])

    return deleted_file

@lambda_method
def get_url_file(event, context, **kwargs):
    pp = event['pathParameters']
    
    s3 = S3(s3config.buckets.upload_bucket,
            s3config.REGION_NAME, s3config.limits_file_size)

    url_file = s3.get_url(pp["key"])

    return url_file
