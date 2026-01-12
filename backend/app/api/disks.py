"""Disk management API endpoints."""

import os
import re
from glob import glob
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.config import settings

router = APIRouter()


class DiskInfo(BaseModel):
    """Information about an array disk."""
    
    id: str  # e.g., "disk1"
    name: str  # e.g., "Disk 1"
    mount_point: str  # e.g., "/mnt/disk1"
    total_bytes: int
    used_bytes: int
    free_bytes: int
    used_percent: float
    filesystem: str | None
    is_mounted: bool
    is_readable: bool
    is_writable: bool


class DiskListResponse(BaseModel):
    """Response containing all detected disks."""
    
    disks: list[DiskInfo]
    total_count: int
    total_capacity_bytes: int
    total_used_bytes: int
    total_free_bytes: int
    average_used_percent: float


def get_disk_info(mount_point: str) -> DiskInfo | None:
    """Get information about a single disk."""
    path = Path(mount_point)
    
    if not path.exists():
        return None
    
    # Extract disk ID from mount point
    match = re.search(r"disk(\d+)", mount_point)
    if not match:
        return None
    
    disk_num = match.group(1)
    disk_id = f"disk{disk_num}"
    disk_name = f"Disk {disk_num}"
    
    try:
        stat = os.statvfs(mount_point)
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bavail * stat.f_frsize
        used = total - free
        used_percent = (used / total * 100) if total > 0 else 0
    except OSError:
        return DiskInfo(
            id=disk_id,
            name=disk_name,
            mount_point=mount_point,
            total_bytes=0,
            used_bytes=0,
            free_bytes=0,
            used_percent=0,
            filesystem=None,
            is_mounted=False,
            is_readable=False,
            is_writable=False,
        )
    
    # Check permissions
    is_readable = os.access(mount_point, os.R_OK)
    is_writable = os.access(mount_point, os.W_OK)
    
    # Try to detect filesystem type
    filesystem = None
    try:
        with open("/proc/mounts") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 3 and parts[1] == mount_point:
                    filesystem = parts[2]
                    break
    except Exception:
        pass
    
    return DiskInfo(
        id=disk_id,
        name=disk_name,
        mount_point=mount_point,
        total_bytes=total,
        used_bytes=used,
        free_bytes=free,
        used_percent=round(used_percent, 2),
        filesystem=filesystem,
        is_mounted=True,
        is_readable=is_readable,
        is_writable=is_writable,
    )


@router.get("", response_model=DiskListResponse)
async def list_disks() -> DiskListResponse:
    """
    List all detected array disks.
    
    Scans for mounted disks matching the pattern /mnt/disk*.
    """
    disk_paths = sorted(glob(settings.disk_mount_pattern))
    
    disks: list[DiskInfo] = []
    for path in disk_paths:
        info = get_disk_info(path)
        if info:
            disks.append(info)
    
    # Sort by disk number
    disks.sort(key=lambda d: int(re.search(r"\d+", d.id).group()))  # type: ignore
    
    total_capacity = sum(d.total_bytes for d in disks)
    total_used = sum(d.used_bytes for d in disks)
    total_free = sum(d.free_bytes for d in disks)
    avg_percent = (total_used / total_capacity * 100) if total_capacity > 0 else 0
    
    return DiskListResponse(
        disks=disks,
        total_count=len(disks),
        total_capacity_bytes=total_capacity,
        total_used_bytes=total_used,
        total_free_bytes=total_free,
        average_used_percent=round(avg_percent, 2),
    )


@router.get("/{disk_id}", response_model=DiskInfo)
async def get_disk(disk_id: str) -> DiskInfo:
    """Get information about a specific disk."""
    mount_point = f"/mnt/{disk_id}"
    
    info = get_disk_info(mount_point)
    if not info:
        raise HTTPException(status_code=404, detail=f"Disk not found: {disk_id}")
    
    return info
