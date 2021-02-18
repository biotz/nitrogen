import os
from pathlib import Path
import boto3


S3_BUCKET = boto3.resource("s3").Bucket(os.environ["S3_BUCKET_NAME"])


def local_image_path(imagefile):
    """Converts an image name to a path"""
    return Path("/app/tests/resources") / f"{imagefile}.jpg"

def cloud_image(image_name):
    """Download a image file and return path to a temporary locataion of it."""
    image_file = f"{image_name}.jpg"
    tmp_file = f"/tmp/{image_file}"
    S3_BUCKET.download_file(image_file, tmp_file)
    return tmp_file
