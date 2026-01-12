# unRAID Array Balancer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![unRAID](https://img.shields.io/badge/unRAID-7.0%2B-orange)](https://unraid.net/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://hub.docker.com/)
[![Status](https://img.shields.io/badge/Status-Alpha-red)](https://github.com/Rayce185/unraid-array-balancer)

A disk balancing tool for unRAID 7+ arrays. Balance disk usage by percentage across your array drives with a modern web interface, smart suggestions, and safety-first design.

![Dashboard Preview](docs/images/dashboard-preview.png)

---

## ⚠️ DISCLAIMER

> **USE AT YOUR OWN RISK.** This software moves files between physical disks.
> While every effort has been made to ensure safe operation:
>
> - **ALWAYS MAINTAIN BACKUPS** of important data
> - This software is provided "AS IS" without warranty of any kind
> - The authors are not responsible for any data loss or corruption
> - Test thoroughly with non-critical data before production use
> - This is **ALPHA** software - expect bugs
>
> By using this software, you acknowledge these risks and accept full responsibility for any consequences.

---

## Features

- 📊 **Dashboard** - Visual overview of all array disks with fill percentages
- 📁 **Dual-Pane File Browser** - Browse and select files with directory size aggregation
- 🎯 **Smart Suggestions** - Auto-generate balance plans to meet target percentages
- 🔄 **Task Queue** - Manage, prioritize, and monitor move operations
- ✅ **Checksum Verification** - Verify file integrity before deleting source
- ⏸️ **Safe Cancellation** - Cancel operations at safe checkpoints
- ↩️ **Undo Capability** - Reverse completed moves within 24 hours
- 🔒 **Mover Integration** - Respects unRAID mover, pauses when mover runs
- 📝 **Comprehensive Logging** - Full audit trail of all operations
- 🔐 **Authentication** - Optional password protection

## Requirements

- **unRAID 7.0.0 or higher**
- **Docker** (included with unRAID)
- Array must be started

## Quick Start

### 1. Install via Docker Compose

Create a new stack in Portainer or use the command line:

```yaml
version: '3.8'

services:
  array-balancer:
    image: ghcr.io/rayce185/unraid-array-balancer:latest
    container_name: array-balancer
    ports:
      - "28787:8080"
    volumes:
      # Mount your array disks (add all your disks)
      - /mnt/disk1:/mnt/disk1
      - /mnt/disk2:/mnt/disk2
      - /mnt/disk3:/mnt/disk3
      # ... add all disks up to disk30 ...
      
      # Required: Share configs
      - /boot/config/shares:/config/shares:ro
      
      # Required: Mover detection
      - /var/run:/var/run:ro
      
      # Required: Persistent data
      - /mnt/user/appdata/array-balancer:/app/data
    environment:
      - PUID=99
      - PGID=100
      - TZ=Europe/Zurich
      - AUTH_USERNAME=admin
      - AUTH_PASSWORD=changeme    # CHANGE THIS!
    restart: unless-stopped
```

### 2. Access the Web UI

Open your browser to: `http://your-unraid-ip:28787`

Default credentials:
- Username: `admin`
- Password: `arraybalancer` (change this immediately!)

### 3. First Run

1. Accept the welcome screen acknowledgments
2. Wait for initial permission check
3. Run an index of your array (read-only, safe)
4. Review your disk usage
5. Use **Dry Run** mode to preview balance plans before executing

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | `99` | User ID (99 = nobody on unRAID) |
| `PGID` | `100` | Group ID (100 = users on unRAID) |
| `TZ` | `UTC` | Timezone |
| `AUTH_ENABLED` | `true` | Enable authentication |
| `AUTH_USERNAME` | `admin` | Login username |
| `AUTH_PASSWORD` | `arraybalancer` | Login password |
| `LOG_LEVEL` | `info` | Logging level (debug/info/warn/error) |
| `DRY_RUN` | `true` | Start in dry-run mode (recommended) |
| `UNDO_RETENTION_HOURS` | `24` | Hours to keep undo records |
| `STRICT_PERMISSIONS` | `true` | Fail on permission errors |

### Volume Mounts

| Container Path | Host Path | Required | Mode |
|----------------|-----------|----------|------|
| `/mnt/disk*` | `/mnt/disk*` | Yes | rw |
| `/config/shares` | `/boot/config/shares` | Yes | ro |
| `/var/run` | `/var/run` | Yes | ro |
| `/app/data` | `/mnt/user/appdata/array-balancer` | Yes | rw |
| `/config/dynamix` | `/boot/config/plugins/dynamix` | No | ro |

## Safety Features

This tool is designed with safety as the top priority:

1. **Dry Run Default** - All operations preview-only until explicitly enabled
2. **Checksum Verification** - Files verified with MD5/SHA256 before source deletion
3. **Mover Awareness** - Automatically pauses when unRAID mover is running
4. **Safe Checkpoints** - Operations can only be cancelled at safe points
5. **Transaction Logging** - Every operation logged for recovery
6. **Permission Verification** - Checks access rights before any operation
7. **Health Monitoring** - Continuous checks during operations

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Technical design and data flow
- [API Reference](docs/API.md) - REST API documentation
- [Safety Guide](docs/SAFETY.md) - How safety features work
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history

## Support

- **Issues**: [GitHub Issues](https://github.com/Rayce185/unraid-array-balancer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Rayce185/unraid-array-balancer/discussions)

Please check existing issues before creating a new one.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by the [Unbalance](https://github.com/jbrodriguez/unbalance) plugin
- Built for the [unRAID](https://unraid.net/) community
- Thanks to all contributors and testers

---

**Note:** This project is not affiliated with Lime Technology (unRAID).
