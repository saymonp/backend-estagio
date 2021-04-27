import logging
import boto3
from botocore.exceptions import ClientError
import uuid

s3_client = boto3.client('s3')

class S3(object):
    self.allowed_mimes = [
      "image/jpeg",
      "image/pjpeg",
      "image/png",
      "3d??"
    ]

    def __init__(self, bucket_name, size_limits):
        self.bucket = bucket_name
        self.limits = size_limits
        

    def upload(self, file_name, object_name):
        object_name = uuid.uuid4()
        try:
            response = s3_client.upload_file(file_name, self.bucket, object_name)
            url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        except ClientError as e:
            logging.error(e)
            return False
        return {"image_url": url, "key": key}

    def delete(self, key):
        s3_client.delete(self.bucket, key)

    def get_url(self, key):
        url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        
        return {"image_url": url, "key": key}