from fastapi import FastAPI
from app.config import settings
from app.logging_conf import setup_logging
from app.endpoints import endpoints

logger = setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

# Include the example router
app.include_router(example.router, prefix="/api", tags=["example"])

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} environment.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")

