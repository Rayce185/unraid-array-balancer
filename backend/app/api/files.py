"""File browser API endpoints."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter()


class FileInfo(BaseModel):
    """Information about a file or directory."""
    
    name: str
    path: str
    is_directory: bool
    size_bytes: int
    modified_at: str
    children_count: int | None = None  # For directories


class DirectoryContents(BaseModel):
    """Contents of a directory."""
    
    path: str
    disk_id: str
    parent_path: str | None
    items: list[FileInfo]
    total_size_bytes: int
    file_count: int
    directory_count: int


@router.get("/{disk_id}", response_model=DirectoryContents)
async def browse_disk(
    disk_id: str,
    path: str = Query("/", description="Path relative to disk root"),
) -> DirectoryContents:
    """
    Browse files on a disk.
    
    Returns directory contents with size information.
    """
    mount_point = Path(f"/mnt/{disk_id}")
    
    if not mount_point.exists():
        raise HTTPException(status_code=404, detail=f"Disk not found: {disk_id}")
    
    # Sanitize path to prevent traversal
    target_path = mount_point / path.lstrip("/")
    
    try:
        target_path = target_path.resolve()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid path")
    
    # Ensure we're still within the disk mount
    if not str(target_path).startswith(str(mount_point)):
        raise HTTPException(status_code=403, detail="Path traversal not allowed")
    
    if not target_path.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    
    if not target_path.is_dir():
        raise HTTPException(status_code=400, detail="Path is not a directory")
    
    items: list[FileInfo] = []
    total_size = 0
    file_count = 0
    dir_count = 0
    
    try:
        for item in sorted(target_path.iterdir()):
            try:
                stat = item.stat()
                is_dir = item.is_dir()
                
                if is_dir:
                    dir_count += 1
                    # TODO: Calculate directory size from index
                    size = 0
                else:
                    file_count += 1
                    size = stat.st_size
                    total_size += size
                
                items.append(FileInfo(
                    name=item.name,
                    path=str(item.relative_to(mount_point)),
                    is_directory=is_dir,
                    size_bytes=size,
                    modified_at=str(stat.st_mtime),
                ))
            except (PermissionError, OSError):
                # Skip files we can't access
                continue
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    relative_path = str(target_path.relative_to(mount_point))
    parent_path = str(target_path.parent.relative_to(mount_point)) if target_path != mount_point else None
    
    return DirectoryContents(
        path=relative_path,
        disk_id=disk_id,
        parent_path=parent_path,
        items=items,
        total_size_bytes=total_size,
        file_count=file_count,
        directory_count=dir_count,
    )
