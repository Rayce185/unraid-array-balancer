"""Task queue API endpoints."""

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class Task(BaseModel):
    """A task in the queue."""
    
    id: int
    type: str
    status: Literal["pending", "queued", "running", "paused", "completed", "failed", "cancelled"]
    priority: Literal["low", "normal", "high", "urgent"]
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    progress_percent: float
    details: dict
    error: str | None


class TaskQueue(BaseModel):
    """Current state of the task queue."""
    
    running: Task | None
    queued: list[Task]
    completed: list[Task]
    is_paused: bool
    pause_reason: str | None


class CreateTaskRequest(BaseModel):
    """Request to create a new task."""
    
    type: str
    priority: Literal["low", "normal", "high", "urgent"] = "normal"
    details: dict


@router.get("", response_model=TaskQueue)
async def get_task_queue() -> TaskQueue:
    """Get the current task queue state."""
    # TODO: Implement actual queue management
    return TaskQueue(
        running=None,
        queued=[],
        completed=[],
        is_paused=False,
        pause_reason=None,
    )


@router.post("", response_model=Task)
async def create_task(request: CreateTaskRequest) -> Task:
    """Create a new task."""
    # TODO: Implement task creation
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int) -> Task:
    """Get a specific task by ID."""
    # TODO: Implement task retrieval
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/cancel")
async def cancel_task(task_id: int) -> dict:
    """Cancel a task (at next safe point)."""
    # TODO: Implement cancellation
    return {
        "status": "accepted",
        "message": "Task will be cancelled at next safe point",
    }


@router.post("/{task_id}/pause")
async def pause_task(task_id: int) -> dict:
    """Pause a running task."""
    # TODO: Implement pause
    return {
        "status": "accepted",
        "message": "Task paused",
    }


@router.post("/{task_id}/resume")
async def resume_task(task_id: int) -> dict:
    """Resume a paused task."""
    # TODO: Implement resume
    return {
        "status": "accepted",
        "message": "Task resumed",
    }


@router.post("/reorder")
async def reorder_tasks(task_ids: list[int]) -> dict:
    """Reorder queued tasks."""
    # TODO: Implement reordering
    return {
        "status": "ok",
        "message": "Tasks reordered",
    }
