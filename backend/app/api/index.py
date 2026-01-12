"""File index API endpoints."""

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class IndexStatus(BaseModel):
    """Status of the file index."""
    
    status: str  # "none", "indexing", "current", "stale"
    last_indexed_at: datetime | None
    total_files: int
    total_size_bytes: int
    index_duration_seconds: float | None
    disks_indexed: list[str]


class IndexProgress(BaseModel):
    """Progress of an ongoing index operation."""
    
    is_running: bool
    current_disk: str | None
    files_processed: int
    total_files_estimate: int
    percent_complete: float
    elapsed_seconds: float
    eta_seconds: float | None


@router.get("/status", response_model=IndexStatus)
async def get_index_status() -> IndexStatus:
    """Get the current status of the file index."""
    # TODO: Implement actual index status checking
    return IndexStatus(
        status="none",
        last_indexed_at=None,
        total_files=0,
        total_size_bytes=0,
        index_duration_seconds=None,
        disks_indexed=[],
    )


@router.get("/progress", response_model=IndexProgress)
async def get_index_progress() -> IndexProgress:
    """Get progress of ongoing index operation."""
    # TODO: Implement actual progress tracking
    return IndexProgress(
        is_running=False,
        current_disk=None,
        files_processed=0,
        total_files_estimate=0,
        percent_complete=0,
        elapsed_seconds=0,
        eta_seconds=None,
    )


@router.post("/start")
async def start_index() -> dict:
    """Start indexing the array."""
    # TODO: Implement actual indexing
    return {
        "status": "accepted",
        "message": "Index operation queued",
    }


@router.post("/cancel")
async def cancel_index() -> dict:
    """Cancel ongoing index operation."""
    # TODO: Implement cancellation
    return {
        "status": "ok",
        "message": "Index cancelled",
    }
