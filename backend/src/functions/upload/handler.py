# backend/src/functions/upload/handler.py
import json
import uuid
from typing import Dict
import os

from lib.s3_manager import S3Manager
from lib.dynamo_manager import DynamoManager
from utils.logger import get_logger

logger = get_logger(__name__)

def handle(event, context) -> Dict:
    try:
        body = json.loads(event['body'])
        file_name = body['fileName']
        file_size = body['fileSize']
        content_type = body['contentType']

        s3_manager = S3Manager()
        dynamo_manager = DynamoManager()

        # Generate unique file ID
        file_id = str(uuid.uuid4())

        # Get upload URL
        upload_data = s3_manager.generate_presigned_url(
            file_name=file_id,
            file_size=file_size,
            content_type=content_type
        )

        # Store file mapping
        dynamo_manager.store_file_mapping(
            file_id=file_id,
            bucket=upload_data['bucket'],
            metadata={
                'original_name': file_name,
                'size': file_size,
                'content_type': content_type
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'fileId': file_id,
                'uploadUrl': upload_data['url'],
                'bucket': upload_data['bucket']
            })
        }
    except Exception as e:
        logger.error(f"Upload handler error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
