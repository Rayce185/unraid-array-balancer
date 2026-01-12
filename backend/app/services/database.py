"""Database initialization and connection management."""

import aiosqlite

from app.services.config import settings

_db: aiosqlite.Connection | None = None


async def get_database() -> aiosqlite.Connection:
    """Get the database connection."""
    global _db
    if _db is None:
        _db = await aiosqlite.connect(settings.database_path)
        _db.row_factory = aiosqlite.Row
    return _db


async def init_database() -> None:
    """Initialize the database schema."""
    db = await get_database()
    
    # Create tables
    await db.executescript("""
        -- Settings table
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Task queue
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            priority TEXT NOT NULL DEFAULT 'normal',
            details TEXT NOT NULL,  -- JSON
            correlation_group TEXT,
            depends_on TEXT,  -- JSON array of task IDs
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_correlation ON tasks(correlation_group);
        
        -- Undo log
        CREATE TABLE IF NOT EXISTS undo_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            operation TEXT NOT NULL,
            source_path TEXT NOT NULL,
            dest_path TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            checksum TEXT,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_valid BOOLEAN DEFAULT TRUE,
            invalidation_reason TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_undo_expires ON undo_log(expires_at);
        CREATE INDEX IF NOT EXISTS idx_undo_valid ON undo_log(is_valid);
        
        -- Operation history
        CREATE TABLE IF NOT EXISTS operation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            operation TEXT NOT NULL,
            source_path TEXT,
            dest_path TEXT,
            file_size INTEGER,
            status TEXT NOT NULL,
            duration_ms INTEGER,
            error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_history_created ON operation_history(created_at);
        
        -- Session table for authentication
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL
        );
        
        CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);
    """)
    
    await db.commit()


async def close_database() -> None:
    """Close the database connection."""
    global _db
    if _db is not None:
        await _db.close()
        _db = None
