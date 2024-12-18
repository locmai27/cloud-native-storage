# backend/src/models/storage_metrics.py
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime

@dataclass
class BucketMetrics:
    bucket_name: str
    total_size: int
    object_count: int
    last_updated: datetime
    
    def is_near_capacity(self, threshold_gb: int = 4000) -> bool:
        # Convert bytes to GB
        current_size_gb = self.total_size / (1024 ** 3)
        return current_size_gb >= threshold_gb * 0.8  # 80% of threshold

@dataclass
class StorageMetrics:
    total_storage: int
    bucket_metrics: List[BucketMetrics]
    
    def get_least_utilized_bucket(self) -> BucketMetrics:
        return min(self.bucket_metrics, 
                  key=lambda x: x.total_size)
    
    def get_most_utilized_bucket(self) -> BucketMetrics:
        return max(self.bucket_metrics, 
                  key=lambda x: x.total_size)
