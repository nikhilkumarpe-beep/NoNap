# NoNap

NoNap is a driver-drowsiness detection prototype with an Expo / React Native client and a Python computer-vision backend.

**Stack:** Python · FastAPI · OpenCV · YOLO · dlib · EAR/MAR · React Native · Expo · TypeScript

## What is implemented

- WebSocket endpoint for receiving JPEG camera frames
- YOLO face detection and dlib 68-point facial landmarks
- Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR) calculations
- CLAHE preprocessing for low-light frames
- A hysteresis state machine to reduce rapid alert-state changes
- A React Native / Expo interface with personal and fleet-oriented screens
- A health endpoint that reports whether the face detector initialized

## Architecture

```text
Camera frame
    │ JPEG over WebSocket
    ▼
FastAPI backend (/detection)
    ├── CLAHE preprocessing
    ├── YOLO face detection
    ├── dlib facial landmarks
    ├── EAR / MAR features
    └── Hysteresis state classification
    │
    ▼
JSON detection result
    │
    ▼
Expo / React Native client
```

## Repository layout

```text
NoNap/
├── app/                 # Expo / React Native client
├── backend/
│   ├── main.py          # FastAPI and WebSocket entry point
│   ├── webcam_server.py # Local webcam preview client
│   ├── pipeline/        # Detection and fatigue feature modules
│   └── requirements.txt
└── scripts/
    └── setup.sh
```

## Requirements

- Python 3.11 recommended
- Node.js and npm
- A working webcam/camera source for live testing
- Model files described below

The backend dependencies include PyTorch, OpenCV, Ultralytics, dlib and SciPy. Installation can take time and may require platform-specific build tools, especially for dlib.

## Setup

Run from the repository root on macOS or Linux:

```bash
bash scripts/setup.sh
```

The script installs backend dependencies, downloads the dlib landmark predictor, and installs the app dependencies using the committed lockfile.

If setup fails on your platform, follow the steps manually.

### Start the backend

```bash
cd backend
.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8765
```

Check health at `http://127.0.0.1:8765/health`.

### Start the mobile app

In a second terminal:

```bash
cd app
npm start
```

Use the Expo CLI to open the app on a supported simulator or device. A physical device must be able to reach the backend host; `localhost` on a phone refers to the phone itself. For a physical device, set `EXPO_PUBLIC_BACKEND_HOST` to your computer's LAN IP before starting Expo, for example `EXPO_PUBLIC_BACKEND_HOST=192.168.1.20 npm start` (replace the example IP with your computer's address).

### Local webcam preview

The optional webcam preview client connects to the backend over WebSocket. Run it on a machine with a webcam and OpenCV GUI support:

```bash
cd backend
.venv/bin/python webcam_server.py
```

## Model limitations

**The current repository does not include trained Vision Transformer weights.** The `ViTAnalyzer` currently uses an EAR/MAR-based fallback score; it is not performing real ViT inference. The backend also requires the YOLO face model file and the dlib landmark predictor to initialize face detection. The health endpoint reports detector initialization status.

This is a prototype for development and evaluation, not a certified driver-safety device. Do not rely on it as the sole means of preventing accidents.

## Configuration and generated files

- Keep credentials and local configuration out of Git.
- Model files and downloaded weights should be treated as setup assets.
- Runtime logs, Python bytecode, virtual environments, and `node_modules` are excluded from version control.

## Engineering concepts

- Real-time image processing
- WebSocket communication
- Face detection and facial landmarks
- EAR/MAR feature engineering
- Temporal smoothing / hysteresis
- Mobile-to-backend integration
- Modular Python code

## Author

**Nikhil Kumar PE**

[GitHub profile](https://github.com/nikhilkumarpe-beep)
