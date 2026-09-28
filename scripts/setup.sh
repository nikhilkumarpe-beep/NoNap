#!/usr/bin/env bash
# Prepare the NoNap backend and Expo app from the repository root.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "Setting up NoNap backend..."
cd "$ROOT_DIR/backend"
"$PYTHON_BIN" -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# dlib's 68-point predictor is required by the current face-landmark pipeline.
mkdir -p models
PREDICTOR="models/shape_predictor_68_face_landmarks.dat"
if [ ! -f "$PREDICTOR" ]; then
  echo "Downloading dlib 68-point landmark predictor..."
  python -c "import urllib.request; urllib.request.urlretrieve('https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2', 'models/shape_predictor_68_face_landmarks.dat.bz2')"
  bzip2 -df models/shape_predictor_68_face_landmarks.dat.bz2
fi

echo "Setting up Expo app..."
cd "$ROOT_DIR/app"
npm ci

echo "Setup complete."
echo "Start backend: cd backend && .venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8765"
echo "Start app:     cd app && npm start"
