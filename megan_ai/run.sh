#!/usr/bin/env bash
set -e
. /venv/bin/activate
echo "[Megan] Starting offline model service..."
exec uvicorn server:app --host 0.0.0.0 --port 8000
