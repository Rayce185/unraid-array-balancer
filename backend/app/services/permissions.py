"""Permission checking service for verifying access rights."""

import os
from dataclasses import dataclass, field
from glob import glob
from pathlib import Path
from typing import Literal

from app.services.config import settings


@dataclass
class PermissionCheck:
    """Result of a single permission check."""
    
    name: str
    description: str
    status: Literal["ok", "warning", "error"]
    error: str | None = None
    details: dict[str, str] = field(default_factory=dict)


@dataclass
class PermissionReport:
    """Complete permission check report."""
    
    running_as_uid: int
    running_as_gid: int
    checks: list[PermissionCheck] = field(default_factory=list)
    
    @property
    def passed_checks(self) -> list[PermissionCheck]:
        """Get all passed checks."""
        return [c for c in self.checks if c.status == "ok"]
    
    @property
    def warning_checks(self) -> list[PermissionCheck]:
        """Get all warning checks."""
        return [c for c in self.checks if c.status == "warning"]
    
    @property
    def failed_checks(self) -> list[PermissionCheck]:
        """Get all failed checks."""
        return [c for c in self.checks if c.status == "error"]
    
    @property
    def has_critical_failures(self) -> bool:
        """Check if there are any critical failures."""
        critical_names = {"disk_read", "config_read", "appdata_write"}
        return any(c.name in critical_names for c in self.failed_checks)
    
    @property
    def all_passed(self) -> bool:
        """Check if all checks passed."""
        return len(self.failed_checks) == 0


class PermissionChecker:
    """Check permissions for all required operations."""
    
    async def check_all(self) -> PermissionReport:
        """Run all permission checks and return a report."""
        report = PermissionReport(
            running_as_uid=os.getuid(),
            running_as_gid=os.getgid(),
        )
        
        # Run all checks
        report.checks.append(await self._check_disk_read())
        report.checks.append(await self._check_disk_write())
        report.checks.append(await self._check_config_read())
        report.checks.append(await self._check_appdata_write())
        report.checks.append(await self._check_mover_status())
        report.checks.append(await self._check_rsync())
        
        return report
    
    async def _check_disk_read(self) -> PermissionCheck:
        """Check read access to all mounted disks."""
        check = PermissionCheck(
            name="disk_read",
            description="Read access to array disks",
            status="ok",
        )
        
        disks = glob(settings.disk_mount_pattern)
        if not disks:
            check.status = "warning"
            check.error = "No disks found matching pattern"
            return check
        
        unreadable = []
        for disk in disks:
            if not os.access(disk, os.R_OK):
                unreadable.append(disk)
            else:
                check.details[disk] = "readable"
        
        if unreadable:
            check.status = "error"
            check.error = f"Cannot read: {', '.join(unreadable)}"
            for disk in unreadable:
                check.details[disk] = "NOT readable"
        
        return check
    
    async def _check_disk_write(self) -> PermissionCheck:
        """Check write access to all mounted disks."""
        check = PermissionCheck(
            name="disk_write",
            description="Write access to array disks",
            status="ok",
        )
        
        disks = glob(settings.disk_mount_pattern)
        if not disks:
            check.status = "warning"
            check.error = "No disks found"
            return check
        
        unwritable = []
        for disk in disks:
            if not os.access(disk, os.W_OK):
                unwritable.append(disk)
            else:
                check.details[disk] = "writable"
        
        if unwritable:
            check.status = "error"
            check.error = f"Cannot write: {', '.join(unwritable)}"
            for disk in unwritable:
                check.details[disk] = "NOT writable"
        
        return check
    
    async def _check_config_read(self) -> PermissionCheck:
        """Check read access to share configuration."""
        check = PermissionCheck(
            name="config_read",
            description="Read access to share configs",
            status="ok",
        )
        
        config_path = settings.share_config_path
        
        if not config_path.exists():
            check.status = "warning"
            check.error = f"Config path not found: {config_path}"
            return check
        
        if not os.access(config_path, os.R_OK):
            check.status = "error"
            check.error = f"Cannot read: {config_path}"
            return check
        
        check.details["path"] = str(config_path)
        return check
    
    async def _check_appdata_write(self) -> PermissionCheck:
        """Check write access to app data directory."""
        check = PermissionCheck(
            name="appdata_write",
            description="Write access to app data",
            status="ok",
        )
        
        data_dir = settings.data_dir
        
        if not data_dir.exists():
            try:
                data_dir.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                check.status = "error"
                check.error = f"Cannot create: {data_dir}"
                return check
        
        if not os.access(data_dir, os.W_OK):
            check.status = "error"
            check.error = f"Cannot write: {data_dir}"
            return check
        
        # Test actual write
        test_file = data_dir / ".write_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            check.status = "error"
            check.error = f"Write test failed: {e}"
            return check
        
        check.details["path"] = str(data_dir)
        return check
    
    async def _check_mover_status(self) -> PermissionCheck:
        """Check ability to read mover status."""
        check = PermissionCheck(
            name="mover_status",
            description="Read mover status",
            status="ok",
        )
        
        # Check /var/run is accessible
        var_run = Path("/var/run")
        if not os.access(var_run, os.R_OK):
            check.status = "warning"
            check.error = "Cannot read /var/run - mover detection may not work"
            return check
        
        check.details["path"] = str(settings.mover_pid_path)
        return check
    
    async def _check_rsync(self) -> PermissionCheck:
        """Check if rsync is available."""
        check = PermissionCheck(
            name="rsync",
            description="rsync availability",
            status="ok",
        )
        
        import shutil
        
        rsync_path = shutil.which("rsync")
        if rsync_path is None:
            check.status = "error"
            check.error = "rsync not found in PATH"
            return check
        
        if not os.access(rsync_path, os.X_OK):
            check.status = "error"
            check.error = f"rsync not executable: {rsync_path}"
            return check
        
        check.details["path"] = rsync_path
        return check
    
    async def check_file_operation(
        self,
        source: Path,
        dest: Path,
    ) -> PermissionCheck:
        """Check permissions for a specific file operation."""
        check = PermissionCheck(
            name="file_operation",
            description=f"Move {source.name}",
            status="ok",
        )
        
        errors = []
        
        # Source must be readable
        if not os.access(source, os.R_OK):
            errors.append(f"Source not readable: {source}")
        
        # Source parent must be writable (for deletion)
        if not os.access(source.parent, os.W_OK):
            errors.append(f"Source directory not writable: {source.parent}")
        
        # Destination parent must exist and be writable
        if not dest.parent.exists():
            errors.append(f"Destination directory doesn't exist: {dest.parent}")
        elif not os.access(dest.parent, os.W_OK):
            errors.append(f"Destination directory not writable: {dest.parent}")
        
        if errors:
            check.status = "error"
            check.error = "; ".join(errors)
        
        return check
