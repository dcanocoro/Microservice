#app/utilities/middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import time
from app.utilities.logging_conf import get_logger, get_technical_logger

logger = get_logger()
technical_logger = get_technical_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para registrar todas las peticiones y respuestas"""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.activity(request, response)
        technical_logger.info(f"Request processed in {process_time:.4f} seconds")  # Log técnico

        return response
