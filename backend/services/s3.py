import logging
import boto3
from botocore.exceptions import ClientError
import uuid
import re
from base64 import b64decode
from sys import getsizeof

from ..config.s3config import s3config
from backend.errors import AppError

s3_client = boto3.client('s3',
                         aws_access_key_id=s3config.AWS_SERVER_PUBLIC_KEY,
                         aws_secret_access_key=s3config.AWS_SERVER_SECRET_KEY,
                         region_name=s3config.REGION_NAME
                         )


class S3(object):

    def __init__(self, bucket_name, region, size_limits):
        self.bucket = bucket_name
        self.limits = size_limits
        self.region = region

    def upload(self, file, object_name, path=None):
        match = re.search("data:(.+/.+);base64,(.+)", file)

        mime = match.group(1)
        base64 = match.group(2)
        

        filedata = b64decode(base64)

        size = getsizeof(filedata) 

        if size > 30000000:
            raise AppError("Data to large").set_code(404)

        key = path + str(uuid.uuid4()) + object_name

        try:
            response = s3_client.put_object(
                Body=filedata, Bucket=self.bucket, Key=key, ACL='public-read')
            url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"

        except ClientError as e:
            logging.error(e)

            return False

        return {"file_url": url, "key": key}

    def delete(self, key):
        s3_client.delete_object(Bucket=self.bucket, Key=key)
        return {"deleted": key}

    def get_url(self, key):
        url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"

        return {"file_url": url, "key": key}
