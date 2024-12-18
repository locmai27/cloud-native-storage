# backend/src/lib/dynamo_manager.py
import boto3
from typing import Dict, List
import os
import time

class DynamoManager:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.environ['FILE_MAPPING_TABLE'])

    def store_file_mapping(self, 
                          file_id: str, 
                          bucket: str, 
                          metadata: Dict) -> None:
        try:
            self.table.put_item(
                Item={
                    'file_id': file_id,
                    'bucket': bucket,
                    'metadata': metadata,
                    'timestamp': int(time.time())
                }
            )
        except Exception as e:
            raise Exception(f"Failed to store file mapping: {str(e)}")

    def get_file_location(self, file_id: str) -> Dict:
        try:
            response = self.table.get_item(Key={'file_id': file_id})
            return response.get('Item')
        except Exception as e:
            raise Exception(f"Failed to retrieve file location: {str(e)}")
