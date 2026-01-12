"""Mover integration API endpoints."""

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.config import settings

router = APIRouter()


class MoverStatus(BaseModel):
    """Status of the unRAID mover."""
    
    is_running: bool
    next_scheduled: datetime | None
    last_run: datetime | None


@router.get("/status", response_model=MoverStatus)
async def get_mover_status() -> MoverStatus:
    """
    Get the current status of the unRAID mover.
    
    Checks for mover.pid to determine if mover is running.
    """
    is_running = False
    
    # Check for mover PID file
    pid_path = settings.mover_pid_path
    if pid_path.exists():
        try:
            pid = int(pid_path.read_text().strip())
            # Check if process is actually running
            proc_path = Path(f"/proc/{pid}")
            is_running = proc_path.exists()
        except (ValueError, PermissionError):
            pass
    
    # TODO: Parse dynamix.cfg for schedule
    next_scheduled = None
    last_run = None
    
    return MoverStatus(
        is_running=is_running,
        next_scheduled=next_scheduled,
        last_run=last_run,
    )


@router.post("/start")
async def start_mover() -> dict:
    """
    Manually trigger the mover.
    
    Requires confirmation as this affects pool/array data movement.
    """
    # TODO: Implement mover triggering
    # Command: /usr/local/sbin/mover start
    return {
        "status": "not_implemented",
        "message": "Mover trigger not yet implemented",
    }
