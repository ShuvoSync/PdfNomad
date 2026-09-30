#!/bin/bash
# start.sh — Run PDF Nomad backend (works on desktop + Termux/mobile)
#
# Usage:
#   bash start.sh              # Run on 0.0.0.0:8000 (accessible from mobile)
#   bash start.sh localhost    # Run on 127.0.0.1:8000 (local only)
#   PORT=9000 bash start.sh    # Custom port

cd "$(dirname "$0")"

HOST="${1:-0.0.0.0}"
PORT="${PORT:-8000}"

echo "Starting PDF Nomad API..."
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Docs: http://$HOST:$PORT/docs"
echo ""

# Use uv if available, otherwise fall back to python
if command -v uv &> /dev/null; then
    uv run python -m uvicorn main:app --host "$HOST" --port "$PORT" --reload
else
    python -m uvicorn main:app --host "$HOST" --port "$PORT" --reload
fi
