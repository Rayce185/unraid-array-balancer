# Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build


# Build backend
FROM python:3.11-alpine AS backend-builder

WORKDIR /build
RUN apk add --no-cache gcc musl-dev libffi-dev

COPY backend/pyproject.toml ./
RUN pip wheel --no-cache-dir --wheel-dir /wheels -e .


# Production image
FROM python:3.11-alpine

LABEL maintainer="Rayce185"
LABEL org.opencontainers.image.source="https://github.com/Rayce185/unraid-array-balancer"
LABEL org.opencontainers.image.description="A disk balancing tool for unRAID 7+ arrays"
LABEL org.opencontainers.image.licenses="MIT"

# Install runtime dependencies
RUN apk add --no-cache \
    rsync \
    curl \
    tzdata \
    && rm -rf /var/cache/apk/*

# Create non-root user (matching unRAID nobody:users)
RUN addgroup -g 100 users || true \
    && adduser -D -u 99 -G users nobody || true

# Set up app directory
WORKDIR /app

# Copy Python wheels and install
COPY --from=backend-builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

# Copy application code
COPY backend/app /app/app

# Copy frontend build
COPY --from=frontend-builder /build/dist /app/frontend

# Create data directory
RUN mkdir -p /app/data/logs && chown -R 99:100 /app/data

# Environment defaults
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PUID=99 \
    PGID=100 \
    TZ=UTC \
    LOG_LEVEL=info \
    AUTH_ENABLED=true \
    AUTH_USERNAME=admin \
    AUTH_PASSWORD=arraybalancer \
    DRY_RUN=true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Expose port
EXPOSE 8080

# Run as nobody by default (can be overridden with PUID/PGID)
USER 99:100

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
