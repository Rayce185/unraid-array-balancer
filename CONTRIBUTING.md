# Contributing to unRAID Array Balancer

First off, thank you for considering contributing! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Response Times](#response-times)

## Code of Conduct

This project adheres to the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details**: unRAID version, Docker version, browser
- **Logs**: Check `/app/data/logs/` in the container

### Suggesting Features

Feature requests are welcome! Please:

- Check if the feature already exists or is planned
- Describe the use case clearly
- Explain why this would benefit other users

### Pull Requests

PRs are welcome for:

- Bug fixes
- Documentation improvements
- Test coverage improvements
- Performance improvements

For new features, please open an issue first to discuss.

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Git
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Rayce185/unraid-array-balancer.git
cd unraid-array-balancer

# Start development environment
docker compose -f docker/docker-compose.dev.yml up

# Access the UI at http://localhost:28787
# API docs at http://localhost:28787/api/docs
```

### Development Without Docker

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8080

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm run test
```

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** from `develop`: `git checkout -b feature/my-feature`
3. **Make your changes** with clear commits
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Run tests** and linting
7. **Push** to your fork
8. **Open a PR** against `develop` branch

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated (if applicable)
- [ ] Changelog entry added (if applicable)
- [ ] No unnecessary files committed

## Style Guidelines

### Python (Backend)

- **Formatter**: Black (line length 100)
- **Linter**: Ruff
- **Type hints**: Required on public functions
- **Docstrings**: Required on classes and public methods

```python
def calculate_balance(
    disks: list[DiskInfo],
    target_percent: float,
) -> BalancePlan:
    """
    Calculate a balance plan for the given disks.
    
    Args:
        disks: List of disk information objects.
        target_percent: Target fill percentage (0-100).
    
    Returns:
        A BalancePlan with suggested file moves.
    
    Raises:
        ValueError: If target_percent is out of range.
    """
```

### TypeScript/Vue (Frontend)

- **Formatter**: Prettier
- **Linter**: ESLint
- **Style**: Vue 3 Composition API with `<script setup>`
- **Types**: TypeScript strict mode

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  diskId: string
  fillPercent: number
}

const props = defineProps<Props>()
const isOverThreshold = computed(() => props.fillPercent > 90)
</script>
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add disk filtering to file browser
fix: correct checksum calculation for large files
docs: update API documentation
test: add tests for balance algorithm
chore: update dependencies
```

## Response Times

This project is maintained by volunteers. Please be patient:

- **Issues**: Reviewed weekly
- **PRs**: Reviewed within 1-2 weeks
- **Security issues**: Prioritized, aim for 48-hour response

## Questions?

- Open a [Discussion](https://github.com/Rayce185/unraid-array-balancer/discussions)
- Check existing documentation

Thank you for contributing! 🙏
