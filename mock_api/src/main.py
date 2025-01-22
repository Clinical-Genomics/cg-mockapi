# mock_api/mock_api/src/main.py

from fastapi import FastAPI

# Import routers
from mock_api.src.freshdesk.router import router as freshdesk_router
from mock_api.src.lims.router import router as lims_router

# Import middleware setup functions
from mock_api.src.middlewares.cors import add_cors_middleware
from mock_api.src.middlewares.logging import add_logging_middleware

app = FastAPI(title="Mock Freshdesk API")

# Add middlewares
add_cors_middleware(app)
add_logging_middleware(app)

# Include routers
app.include_router(freshdesk_router)
app.include_router(lims_router)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
