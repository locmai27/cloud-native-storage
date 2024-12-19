# backend/src/lib/s3_manager.py
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional
import os

class S3Manager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.default_bucket = os.environ['DEFAULT_BUCKET']

    def generate_presigned_url(self, 
                             file_name: str, 
                             file_size: int, 
                             content_type: str) -> Dict:
        """
        Generate a presigned URL for uploading a file to S3
        """
        if file_size > 100 * 1024 * 1024:  # 100 MB limit
            raise ValueError("File size exceeds the 100 MB limit.")
        try:
            url = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.default_bucket,
                    'Key': file_name,
                    'ContentType': content_type
                },
                ExpiresIn=3600
            )
            return {'url': url, 'bucket': self.default_bucket}
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def get_object_size(self, bucket: str, key: str) -> Optional[int]:
        """
        Get the size of an object in S3
        """
        try:
            response = self.s3_client.head_object(Bucket=bucket, Key=key)
            return response['ContentLength']
        except ClientError:
            return None
