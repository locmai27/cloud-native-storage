# backend/src/lib/cloudfront_manager.py
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional, List
import os
import json
import time
from datetime import datetime, timezone, timedelta

class CloudFrontManager:
    def __init__(self):
        self.cloudfront_client = boto3.client('cloudfront')
        self.s3_client = boto3.client('s3')
        self.distribution_id = os.environ.get('CLOUDFRONT_DISTRIBUTION_ID')
        self.domain_name = os.environ.get('CLOUDFRONT_DOMAIN_NAME')

    def create_distribution(self, bucket_name: str) -> Dict:
        """
        Create a new CloudFront distribution for an S3 bucket
        """
        try:
            origin_id = f'S3-{bucket_name}'
            
            distribution_config = {
                'CallerReference': str(time.time()),
                'Origins': {
                    'Quantity': 1,
                    'Items': [
                        {
                            'Id': origin_id,
                            'DomainName': f'{bucket_name}.s3.amazonaws.com',
                            'S3OriginConfig': {
                                'OriginAccessIdentity': ''  # Will be updated after OAI creation
                            }
                        }
                    ]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': origin_id,
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'AllowedMethods': {
                        'Quantity': 2,
                        'Items': ['GET', 'HEAD'],
                        'CachedMethods': {
                            'Quantity': 2,
                            'Items': ['GET', 'HEAD']
                        }
                    },
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {
                            'Forward': 'none'
                        }
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 86400,
                    'MaxTTL': 31536000,
                    'Compress': True
                },
                'Comment': f'Distribution for {bucket_name}',
                'Enabled': True,
                'PriceClass': 'PriceClass_100'
            }

            # Create Origin Access Identity (OAI)
            oai_response = self.cloudfront_client.create_cloud_front_origin_access_identity(
                CloudFrontOriginAccessIdentityConfig={
                    'CallerReference': str(time.time()),
                    'Comment': f'OAI for {bucket_name}'
                }
            )
            
            oai_id = oai_response['CloudFrontOriginAccessIdentity']['Id']
            distribution_config['Origins']['Items'][0]['S3OriginConfig']['OriginAccessIdentity'] = f'origin-access-identity/cloudfront/{oai_id}'

            # Create the distribution
            response = self.cloudfront_client.create_distribution(
                DistributionConfig=distribution_config
            )

            # Update bucket policy to allow CloudFront access
            self._update_bucket_policy(bucket_name, oai_id)

            return {
                'distribution_id': response['Distribution']['Id'],
                'domain_name': response['Distribution']['DomainName']
            }

        except ClientError as e:
            raise Exception(f"Failed to create CloudFront distribution: {str(e)}")

    def generate_signed_url(self, file_key: str, expiration: int = 3600) -> str:
        """
        Generate a signed URL for private content
        """
        try:
            if not self.distribution_id or not self.domain_name:
                raise ValueError("CloudFront distribution ID and domain name must be configured")

            key_pair_id = os.environ.get('CLOUDFRONT_KEY_PAIR_ID')
            private_key = os.environ.get('CLOUDFRONT_PRIVATE_KEY')

            if not key_pair_id or not private_key:
                raise ValueError("CloudFront key pair ID and private key must be configured")

            signer = boto3.client('cloudfront').get_signer(
                key_pair_id=key_pair_id,
                private_key_string=private_key
            )

            # Using timezone-aware datetime
            date_less_than = datetime.now(timezone.utc) + timedelta(seconds=expiration)

            signed_url = signer.generate_presigned_url(
                f'https://{self.domain_name}/{file_key}',
                date_less_than=date_less_than
            )

            return signed_url

        except Exception as e:
            raise Exception(f"Failed to generate signed URL: {str(e)}")

    def get_distribution_config(self) -> Dict:
        """
        Get the current distribution configuration
        """
        try:
            response = self.cloudfront_client.get_distribution_config(
                Id=self.distribution_id
            )
            return response['DistributionConfig']

        except ClientError as e:
            raise Exception(f"Failed to get distribution config: {str(e)}")

    def update_distribution_config(self, config_updates: Dict) -> None:
        """
        Update distribution configuration
        """
        try:
            current_config = self.get_distribution_config()
            etag = self.cloudfront_client.get_distribution(Id=self.distribution_id)['ETag']

            # Update the configuration
            updated_config = {**current_config, **config_updates}

            self.cloudfront_client.update_distribution(
                DistributionConfig=updated_config,
                Id=self.distribution_id,
                IfMatch=etag
            )

        except ClientError as e:
            raise Exception(f"Failed to update distribution config: {str(e)}")

    def update_bucket_policy(self, bucket_name: str, oai_id: str) -> None:
        """
        Update S3 bucket policy to allow CloudFront access
        """
        try:
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AllowCloudFrontAccess",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": f"arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {oai_id}"
                        },
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            }

            self.s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(bucket_policy)
            )

        except ClientError as e:
            raise Exception(f"Failed to update bucket policy: {str(e)}")

    def get_cache_statistics(self, start_time: datetime, end_time: datetime) -> Dict:
        """
        Get cache statistics for the distribution
        """
        try:
            response = self.cloudfront_client.get_distribution_statistics(
                Id=self.distribution_id,
                StartTime=start_time,
                EndTime=end_time
            )
            return {
                'requests': response['Statistics']['Requests'],
                'bytes_downloaded': response['Statistics']['BytesDownloaded'],
                'hits': response['Statistics']['Hits'],
                'misses': response['Statistics']['Misses']
            }

        except ClientError as e:
            raise Exception(f"Failed to get cache statistics: {str(e)}")
