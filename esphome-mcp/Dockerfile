FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

# Build and install esphome-mcp
ARG BUILD_VERSION=main
RUN uv pip install --system --no-cache "git+https://github.com/frzzyone/ESPHome-MCP-HA-App.git"

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

EXPOSE 8080

ENTRYPOINT ["/app/run.sh"]
