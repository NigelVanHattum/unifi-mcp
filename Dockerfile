FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cache layer)
COPY pyproject.toml .
RUN pip install --no-cache-dir httpx "mcp>=1.0.0"

# Copy source
COPY server.py client.py ./
COPY tools/ tools/

# Config can be mounted at /config/config.json
# Or passed via UNIFI_HOST / UNIFI_API_KEY / UNIFI_VERIFY_SSL env vars
VOLUME ["/config"]

ENTRYPOINT ["python", "server.py"]
