from ..util import dict_to_namedtuple
from ..env import AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY, REGION_NAME


config = {
"buckets": {"upload_bucket": "estagio-uploads"},
"limits_file_size": {"image": 50 * 1024, "model3d": 50 * 1024 * 1024},
"AWS_SERVER_PUBLIC_KEY": AWS_SERVER_PUBLIC_KEY,
"AWS_SERVER_SECRET_KEY": AWS_SERVER_SECRET_KEY,
"REGION_NAME": REGION_NAME
}

s3config = dict_to_namedtuple("s3", config)



    