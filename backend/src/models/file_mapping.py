# backend/src/models/file_mapping.py
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime

@dataclass
class FileMapping:
    file_id: str
    bucket_name: str
    original_name: str
    size: int
    content_type: str
    created_at: datetime
    metadata: Optional[Dict] = None
    
    def to_dynamo_item(self) -> Dict:
        return {
            'file_id': self.file_id,
            'bucket_name': self.bucket_name,
            'original_name': self.original_name,
            'size': self.size,
            'content_type': self.content_type,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata or {}
        }
    
    @classmethod
    def from_dynamo_item(cls, item: Dict) -> 'FileMapping':
        return cls(
            file_id=item['file_id'],
            bucket_name=item['bucket_name'],
            original_name=item['original_name'],
            size=item['size'],
            content_type=item['content_type'],
            created_at=datetime.fromisoformat(item['created_at']),
            metadata=item.get('metadata', {})
        )
