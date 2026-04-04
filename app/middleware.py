import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("finance-backend")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate execution time
        process_time = time.time() - start_time
        
        # Log the request details
        logger.info(
            f"Method: {request.method} "
            f"Endpoint: {request.url.path} "
            f"StatusCode: {response.status_code} "
            f"ExecutionTime: {process_time:.4f}s"
        )
        
        return response
