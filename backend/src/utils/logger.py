# backend/src/utils/logger.py
import logging
import json
from typing import Any, Dict
import os

class CustomLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
        
        # Add custom formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add console handler if not in production
        if os.environ.get('ENVIRONMENT') != 'production':
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def _format_message(self, message: str, extra: Dict[str, Any] = None) -> str:
        if extra:
            return f"{message} | {json.dumps(extra)}"
        return message
    
    def info(self, message: str, extra: Dict[str, Any] = None) -> None:
        self.logger.info(self._format_message(message, extra))
    
    def error(self, message: str, extra: Dict[str, Any] = None) -> None:
        self.logger.error(self._format_message(message, extra))
    
    def warning(self, message: str, extra: Dict[str, Any] = None) -> None:
        self.logger.warning(self._format_message(message, extra))
    
    def debug(self, message: str, extra: Dict[str, Any] = None) -> None:
        self.logger.debug(self._format_message(message, extra))

def get_logger(name: str) -> CustomLogger:
    return CustomLogger(name)
