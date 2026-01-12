"""Application configuration settings."""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    debug: bool = False
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    
    # Paths
    data_dir: Path = Path("/app/data")
    log_dir: Path = Path("/app/data/logs")
    
    # Authentication
    auth_enabled: bool = True
    auth_username: str = "admin"
    auth_password: str = "arraybalancer"
    secret_key: str = "change-me-in-production-use-a-long-random-string"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # User/Group
    puid: int = 99  # nobody
    pgid: int = 100  # users
    
    # Operation settings
    dry_run: bool = True
    undo_retention_hours: int = 24
    strict_permissions: bool = True
    
    # Indexing
    index_threads_fast_percent: int = 75  # % of free threads for <5min jobs
    index_threads_slow_percent: int = 50  # % of free threads for >5min jobs
    index_chunk_size: int = 10000  # Files per progress update
    
    # Disk detection
    disk_mount_pattern: str = "/mnt/disk*"
    share_config_path: Path = Path("/config/shares")
    mover_pid_path: Path = Path("/var/run/mover.pid")
    dynamix_config_path: Path = Path("/config/dynamix/dynamix.cfg")
    
    # Safety
    max_move_size_gb: int = 500  # Warn for moves larger than this
    checksum_algorithm: Literal["md5", "sha256"] = "sha256"
    
    @property
    def database_path(self) -> Path:
        """Get the database file path."""
        return self.data_dir / "state.db"
    
    @property
    def index_database_path(self) -> Path:
        """Get the index database file path."""
        return self.data_dir / "index.db"


settings = Settings()

# Ensure directories exist
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.log_dir.mkdir(parents=True, exist_ok=True)
