#!/usr/bin/env bash
# Start the NoNap backend. Run the Expo app separately from app/.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$ROOT_DIR/backend/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
  echo "Backend environment not found. Run: bash scripts/setup.sh"
  exit 1
fi

cd "$ROOT_DIR/backend"
exec "$PYTHON" -m uvicorn main:app --host 0.0.0.0 --port 8765
