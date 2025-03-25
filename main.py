from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.utilities.logging_conf import get_logger
from app.utilities.middleware import LoggingMiddleware 

# Importar endpoints
from app.endpoints.public import router as public_router
from app.endpoints.private import router as private_router
from app.endpoints.external import router as external_router

logger = get_logger()

app = FastAPI(title=settings.PROJECT_NAME)

# Orden de middlewares: primero logging, luego seguridad
app.add_middleware(LoggingMiddleware)

# (Opcional) Si es necesario, configurar CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o limitar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los endpoints con sus respectivos prefijos y tags
app.include_router(public_router, prefix="/api/v1/public", tags=["Public Endpoints"])
app.include_router(private_router, prefix="/api/v1/private", tags=["Private Endpoints"])
app.include_router(external_router, prefix="/api/v1/external", tags=["External"])

@app.on_event("startup")
async def on_startup():
    logger.info(f"Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} environment...")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")
