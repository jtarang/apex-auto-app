# syntax=docker/dockerfile:1
# Use Python 3.13 slim as the base image
FROM python:3.13-slim

# Install uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./

ENV UV_COMPILE_BYTECODE=1
ENV UV_PROJECT_ENVIRONMENT="/usr/local"

RUN uv sync --frozen --no-dev --no-install-project

COPY ./mcp_server .

# Run the FastMCP mcp_server
CMD ["fastmcp", "run", "apex_auto_mcp.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8100"]