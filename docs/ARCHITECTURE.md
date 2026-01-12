# Architecture

This document describes the technical architecture of unRAID Array Balancer.

## Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Docker Container                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  Frontend (Vue 3)                  Backend (FastAPI)                    │
│  ┌─────────────────────┐          ┌────────────────────────┐           │
│  │ Dashboard           │    ←→    │ REST API               │           │
│  │ File Browser        │          │ ├── /api/disks         │           │
│  │ Task Queue          │          │ ├── /api/files         │           │
│  │ Settings            │          │ ├── /api/tasks         │           │
│  └─────────────────────┘          │ ├── /api/index         │           │
│                                    │ ├── /api/mover         │           │
│                                    │ └── /api/health        │           │
│                                    └────────────────────────┘           │
│                                              │                          │
│                                    ┌─────────┴─────────┐               │
│                                    │ SQLite Database   │               │
│                                    │ • Task queue      │               │
│                                    │ • Undo log        │               │
│                                    │ • File index      │               │
│                                    └───────────────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            │                        │                        │
       /mnt/disk*              /boot/config/            /var/run/
       (array)                 (shares)                 (mover.pid)
```

## Components

### Backend (Python/FastAPI)

**Location:** `backend/app/`

- **main.py** - FastAPI application entry point
- **api/** - REST API endpoints
  - `health.py` - Health check and permissions
  - `auth.py` - Authentication
  - `disks.py` - Disk information
  - `files.py` - File browser
  - `index.py` - File indexing
  - `mover.py` - Mover integration
  - `tasks.py` - Task queue management
- **services/** - Business logic
  - `config.py` - Configuration settings
  - `database.py` - SQLite database
  - `permissions.py` - Permission checking
  - `indexer.py` - File indexing (Phase 1)
  - `balancer.py` - Balance algorithm (Phase 2)
  - `executor.py` - File move execution (Phase 3)
- **models/** - Data models

### Frontend (Vue 3/TypeScript)

**Location:** `frontend/src/`

- **App.vue** - Main application component
- **components/** - Reusable UI components
- **views/** - Page components
- **stores/** - Pinia state management
- **router/** - Vue Router configuration

### Database (SQLite)

**Location:** `/app/data/state.db`

Tables:
- `settings` - User configuration
- `tasks` - Task queue
- `undo_log` - Undo records
- `operation_history` - Audit log
- `sessions` - Authentication sessions

## Data Flow

### Disk Detection

1. Container starts
2. Scan `/mnt/disk*` for mounted disks
3. Read `statvfs` for space information
4. Parse `/proc/mounts` for filesystem type
5. Return disk list via API

### File Indexing

1. User initiates index
2. Detect available CPU threads
3. Calculate thread limit (75%/<5min, 50%/>5min)
4. Parallel scan of all disks
5. Store in SQLite with FTS5
6. Calculate directory sizes

### Balance Planning (Dry Run)

1. Load disk information
2. Calculate target percentages
3. Generate move suggestions
4. Validate against share rules
5. Display preview to user

### File Move Execution

1. Create task in queue
2. Verify permissions
3. Copy with rsync
4. Verify checksum
5. Delete source (if verified)
6. Update index
7. Log to undo record

## Configuration

### Environment Variables

See `backend/app/services/config.py` for all settings.

Key settings:
- `PUID/PGID` - User/group for file operations
- `AUTH_*` - Authentication settings
- `DRY_RUN` - Enable/disable actual moves
- `STRICT_PERMISSIONS` - Fail on permission errors

### Volume Mounts

| Path | Purpose | Mode |
|------|---------|------|
| `/mnt/disk*` | Array disks | rw |
| `/config/shares` | Share configs | ro |
| `/var/run` | Mover status | ro |
| `/app/data` | App data | rw |

## Security

- Authentication via JWT tokens
- Bcrypt password hashing
- Path traversal prevention
- No shell injection (subprocess lists only)
- Rate limiting on login

## Error Handling

- All operations logged
- Graceful degradation on permission errors
- Safe cancellation points
- Undo capability for moves
