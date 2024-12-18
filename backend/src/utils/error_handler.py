# backend/src/utils/error_handler.py
from typing import Dict, Any, Optional
import traceback
from .logger import get_logger

logger = get_logger(__name__)

class StorageError(Exception):
    def __init__(self, message: str, error_code: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}

class ErrorHandler:
    ERROR_CODES = {
        'STORAGE_FULL': 'S001',
        'FILE_NOT_FOUND': 'S002',
        'UPLOAD_FAILED': 'S003',
        'INVALID_FILE': 'S004',
        'BUCKET_ERROR': 'S005'
    }
    
    @staticmethod
    def handle_error(error: Exception) -> Dict[str, Any]:
        """
        Handles different types of errors and returns appropriate response
        """
        if isinstance(error, StorageError):
            logger.error(str(error), extra={
                'error_code': error.error_code,
                'details': error.details
            })
            return {
                'statusCode': 400,
                'body': {
                    'error': str(error),
                    'error_code': error.error_code,
                    'details': error.details
                }
            }
        
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(error)}", extra={
            'traceback': traceback.format_exc()
        })
        return {
            'statusCode': 500,
            'body': {
                'error': 'Internal server error',
                'error_code': 'S999'
            }
        }
    
    @staticmethod
    def validate_file(file_size: int, content_type: str) -> None:
        """
        Validates file parameters
        """
        if file_size <= 0:
            raise StorageError(
                message="Invalid file size",
                error_code=ErrorHandler.ERROR_CODES['INVALID_FILE'],
                details={'size': file_size}
            )
        
        allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
        if content_type not in allowed_types:
            raise StorageError(
                message="Invalid file type",
                error_code=ErrorHandler.ERROR_CODES['INVALID_FILE'],
                details={'content_type': content_type}
            )
