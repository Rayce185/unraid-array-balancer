"""Health check API endpoints."""

import time
from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app import __version__

router = APIRouter()

_start_time = time.time()


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: Literal["healthy", "degraded", "unhealthy"]
    version: str
    uptime_seconds: int
    array_status: Literal["online", "offline", "unknown"]
    index_status: Literal["current", "stale", "indexing", "none"]
    queue_status: Literal["idle", "running", "paused"]
    permissions_ok: bool
    warnings: list[str]


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request) -> HealthResponse:
    """
    Get application health status.
    
    This endpoint is used for Docker health checks and monitoring.
    """
    warnings: list[str] = []
    status: Literal["healthy", "degraded", "unhealthy"] = "healthy"
    
    # Check permission report from startup
    permission_report = getattr(request.app.state, "permission_report", None)
    permissions_ok = True
    
    if permission_report:
        if permission_report.has_critical_failures:
            status = "unhealthy"
            permissions_ok = False
            warnings.append("Critical permission failures")
        elif permission_report.warning_checks:
            status = "degraded"
            for check in permission_report.warning_checks:
                warnings.append(f"Permission warning: {check.name}")
    
    # TODO: Check array status
    array_status: Literal["online", "offline", "unknown"] = "unknown"
    
    # TODO: Check index status
    index_status: Literal["current", "stale", "indexing", "none"] = "none"
    
    # TODO: Check queue status
    queue_status: Literal["idle", "running", "paused"] = "idle"
    
    return HealthResponse(
        status=status,
        version=__version__,
        uptime_seconds=int(time.time() - _start_time),
        array_status=array_status,
        index_status=index_status,
        queue_status=queue_status,
        permissions_ok=permissions_ok,
        warnings=warnings,
    )


@router.get("/permissions")
async def get_permissions(request: Request) -> dict:
    """Get detailed permission check results."""
    report = getattr(request.app.state, "permission_report", None)
    
    if not report:
        return {"error": "Permission report not available"}
    
    return {
        "running_as_uid": report.running_as_uid,
        "running_as_gid": report.running_as_gid,
        "all_passed": report.all_passed,
        "has_critical_failures": report.has_critical_failures,
        "checks": [
            {
                "name": c.name,
                "description": c.description,
                "status": c.status,
                "error": c.error,
                "details": c.details,
            }
            for c in report.checks
        ],
    }
