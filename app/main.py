from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging_conf import get_logger

# Import routers
from app.endpoints.public import router as public_router
from app.endpoints.private import router as private_router
from app.endpoints.auth import router as auth_router
from app.endpoints.external import router as external_router

logger = get_logger()

app = FastAPI(title=settings.PROJECT_NAME)

# (Optional) Configure CORS if needed:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or limit to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your endpoints with versioning and tags
app.include_router(public_router, prefix="/api/v1/public", tags=["Public Endpoints"])
app.include_router(private_router, prefix="/api/v1/private", tags=["Private Endpoints"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(external_router, prefix="/api/v1/external", tags=["External"])

@app.on_event("startup")
async def on_startup():
    logger.info(f"Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} environment...")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")
