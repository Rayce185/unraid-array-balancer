# Project Handover Guide

## For Future Maintainers

This project was created by [@Rayce185](https://github.com/Rayce185) with the intention of eventually handing it over to a more experienced maintainer once the project is stable and proven.

## Current Status

- [ ] Alpha testing complete
- [ ] Beta testing complete
- [ ] v1.0.0 released
- [ ] **Looking for maintainer**

## Project Goals

1. **Primary**: A working disk balancer for personal use
2. **Secondary**: A community tool others can benefit from
3. **Long-term**: Hand over to dedicated maintainer(s)

## To Take Over This Project

If you're interested in maintaining this project:

1. **Fork the repository** to your account
2. **Contact @Rayce185** via GitHub to discuss handover
3. **Review the codebase** - see Architecture section below
4. **Update references**:
   - `CODEOWNERS` file
   - Docker image references in documentation
   - GitHub Actions secrets (for publishing)
5. **Announce** new maintainership on unRAID forums/Discord

## Architecture Overview

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for full technical documentation.

### Key Technologies

| Component | Technology | Why |
|-----------|------------|-----|
| Backend | Python 3.11+ / FastAPI | Modern async API, type hints, auto-docs |
| Frontend | Vue 3 / TypeScript | Reactive UI, type safety |
| Database | SQLite | Simple, no separate service needed |
| Container | Docker / Alpine | Lightweight, standard deployment |

### Key Files

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── api/
│   │   ├── disks.py         # Disk endpoints
│   │   ├── files.py         # File browser endpoints
│   │   ├── tasks.py         # Task queue endpoints
│   │   └── auth.py          # Authentication
│   ├── services/
│   │   ├── indexer.py       # File indexing service
│   │   ├── balancer.py      # Balance algorithm
│   │   ├── executor.py      # File move execution
│   │   └── mover.py         # unRAID mover integration
│   └── models/
│       └── schemas.py       # Pydantic models

frontend/
├── src/
│   ├── App.vue              # Main application
│   ├── views/
│   │   ├── Dashboard.vue    # Main dashboard
│   │   ├── FileBrowser.vue  # File browser
│   │   └── TaskQueue.vue    # Task management
│   └── stores/
│       └── main.ts          # Pinia state store
```

### Database Schema

SQLite database at `/app/data/state.db`:

- `files` - File index (path, size, mtime, disk_id)
- `tasks` - Task queue (id, type, status, details)
- `undo_log` - Undo records (source, dest, checksum)
- `settings` - User settings

## Known Issues / Technical Debt

(Maintained list - update as needed)

| Issue | Priority | Notes |
|-------|----------|-------|
| TBD | | |

## Release Process

1. Update version in `pyproject.toml` and `package.json`
2. Update `CHANGELOG.md`
3. Create PR to `main` from `develop`
4. After merge, tag with version: `git tag v0.1.0`
5. Push tag: `git push origin v0.1.0`
6. GitHub Actions will build and publish Docker image

## Infrastructure

| Service | Purpose | Notes |
|---------|---------|-------|
| GitHub Actions | CI/CD | Builds Docker images on tag |
| GitHub Container Registry | Docker images | `ghcr.io/rayce185/unraid-array-balancer` |

To transfer:
1. Update GitHub Actions secrets
2. Update image registry references
3. Update CODEOWNERS

## Contact

- **Original Author**: [@Rayce185](https://github.com/Rayce185)
- **Method**: GitHub Issues or Discussions

## Thank You

If you're reading this because you're taking over maintenance - thank you! This project was built to help the unRAID community, and I'm grateful someone is continuing that mission.

---

*Last updated: January 2025*
