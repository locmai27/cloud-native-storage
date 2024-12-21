# backend/tests/conftest.py
# import pytest
# import boto3
# from moto import mock_s3

# @pytest.fixture(autouse=True)
# def aws_credentials():
#     """Mocked AWS Credentials"""
#     import os
#     os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
#     os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
#     os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

# @pytest.fixture
# def s3():
#     with mock_s3():
#         s3_client = boto3.client('s3')
#         # Create test bucket
#         s3_client.create_bucket(
#             Bucket='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
#             CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
#         )
#         yield s3_client
