"""Main FastAPI application for unRAID Array Balancer."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth, disks, files, health, index, mover, tasks
from app.services.config import settings
from app.services.database import init_database
from app.services.permissions import PermissionChecker

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y.%m.%d_%H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    logger.info("Starting unRAID Array Balancer v%s", app.version)
    
    # Initialize database
    await init_database()
    logger.info("Database initialized")
    
    # Check permissions
    checker = PermissionChecker()
    report = await checker.check_all()
    
    if report.has_critical_failures:
        logger.error("Critical permission failures detected!")
        for check in report.failed_checks:
            logger.error("  - %s: %s", check.name, check.error)
    else:
        logger.info("Permission checks passed")
    
    # Store permission report for API access
    app.state.permission_report = report
    
    yield
    
    logger.info("Shutting down unRAID Array Balancer")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="unRAID Array Balancer",
        description="A disk balancing tool for unRAID 7+ arrays",
        version="0.1.0-alpha",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, configure appropriately
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(disks.router, prefix="/api/disks", tags=["Disks"])
    app.include_router(files.router, prefix="/api/files", tags=["Files"])
    app.include_router(index.router, prefix="/api/index", tags=["Index"])
    app.include_router(mover.router, prefix="/api/mover", tags=["Mover"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
    
    # Serve frontend static files (in production)
    frontend_path = Path("/app/frontend")
    if frontend_path.exists():
        app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle uncaught exceptions."""
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=settings.debug,
    )
