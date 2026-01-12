# API Reference

Base URL: `http://localhost:28787/api`

Interactive documentation: `http://localhost:28787/api/docs`

## Authentication

Authentication is enabled by default. Use HTTP Basic Auth or obtain a JWT token.

### POST /auth/login

Authenticate and receive a JWT token.

**Request:**
```json
{
  "username": "admin",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_at": "2025-01-13T12:00:00Z"
}
```

## Health

### GET /health

Get application health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0-alpha",
  "uptime_seconds": 3600,
  "array_status": "online",
  "index_status": "current",
  "queue_status": "idle",
  "permissions_ok": true,
  "warnings": []
}
```

### GET /permissions

Get detailed permission check results.

**Response:**
```json
{
  "running_as_uid": 99,
  "running_as_gid": 100,
  "all_passed": true,
  "has_critical_failures": false,
  "checks": [
    {
      "name": "disk_read",
      "description": "Read access to array disks",
      "status": "ok",
      "error": null,
      "details": {
        "/mnt/disk1": "readable",
        "/mnt/disk2": "readable"
      }
    }
  ]
}
```

## Disks

### GET /disks

List all detected array disks.

**Response:**
```json
{
  "disks": [
    {
      "id": "disk1",
      "name": "Disk 1",
      "mount_point": "/mnt/disk1",
      "total_bytes": 4000000000000,
      "used_bytes": 3400000000000,
      "free_bytes": 600000000000,
      "used_percent": 85.0,
      "filesystem": "xfs",
      "is_mounted": true,
      "is_readable": true,
      "is_writable": true
    }
  ],
  "total_count": 14,
  "total_capacity_bytes": 126000000000000,
  "total_used_bytes": 100000000000000,
  "total_free_bytes": 26000000000000,
  "average_used_percent": 79.4
}
```

### GET /disks/{disk_id}

Get information about a specific disk.

**Parameters:**
- `disk_id` - Disk identifier (e.g., "disk1")

## Files

### GET /files/{disk_id}

Browse files on a disk.

**Parameters:**
- `disk_id` - Disk identifier
- `path` (query) - Path relative to disk root (default: "/")

**Response:**
```json
{
  "path": "media/movies",
  "disk_id": "disk1",
  "parent_path": "media",
  "items": [
    {
      "name": "movie.mkv",
      "path": "media/movies/movie.mkv",
      "is_directory": false,
      "size_bytes": 45000000000,
      "modified_at": "1704067200.0"
    }
  ],
  "total_size_bytes": 450000000000,
  "file_count": 100,
  "directory_count": 10
}
```

## Index

### GET /index/status

Get the current status of the file index.

### GET /index/progress

Get progress of ongoing index operation.

### POST /index/start

Start indexing the array. Returns immediately, indexing runs in background.

### POST /index/cancel

Cancel ongoing index operation.

## Mover

### GET /mover/status

Get the current status of the unRAID mover.

**Response:**
```json
{
  "is_running": false,
  "next_scheduled": "2025-01-13T03:00:00Z",
  "last_run": "2025-01-12T03:00:00Z"
}
```

### POST /mover/start

Manually trigger the mover.

## Tasks

### GET /tasks

Get the current task queue state.

**Response:**
```json
{
  "running": null,
  "queued": [],
  "completed": [],
  "is_paused": false,
  "pause_reason": null
}
```

### POST /tasks

Create a new task.

**Request:**
```json
{
  "type": "move_file",
  "priority": "normal",
  "details": {
    "source": "/mnt/disk1/media/movie.mkv",
    "destination": "/mnt/disk2/media/movie.mkv"
  }
}
```

### GET /tasks/{task_id}

Get a specific task by ID.

### POST /tasks/{task_id}/cancel

Cancel a task (at next safe point).

### POST /tasks/{task_id}/pause

Pause a running task.

### POST /tasks/{task_id}/resume

Resume a paused task.

### POST /tasks/reorder

Reorder queued tasks.

**Request:**
```json
{
  "task_ids": [3, 1, 2]
}
```

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message here"
}
```

Common status codes:
- `400` - Bad request (invalid input)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (permission denied)
- `404` - Not found
- `500` - Internal server error
- `501` - Not implemented
