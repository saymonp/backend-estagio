from ..util import dict_to_namedtuple


config = {
"buckets": {"upload_bucket": "estagio-bucket"},
"limits_file_size": {"image": 50 * 1024, "model3d": 50 * 1024 * 1024}
}

s3config = dict_to_namedtuple("s3", config)



    