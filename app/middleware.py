from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import json
from app.logging_conf import get_logger

logger = get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses"""
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        log_data = {
            "message": "Request processed",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "response_time": f"{process_time:.2f}s"
        }
        
        if response.status_code >= 400:
            logger.warning(json.dumps(log_data))
        else:
            logger.info(json.dumps(log_data))
        
        return response
