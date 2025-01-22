import logging

from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logging.info("Request: %s %s", request.method, request.url)
        response = await call_next(request)
        logging.info("Response: %s", response.status_code)
        return response


def add_logging_middleware(app):
    app.add_middleware(LoggingMiddleware)
