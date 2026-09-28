# NoNap

A real-time driver drowsiness detection system combining a mobile interface, computer-vision inference, and a web presentation layer.

**Stack:** React Native / Expo · Python · YOLOv8 · Vision Transformer (ViT) · Next.js

## Project overview

NoNap is designed to detect signs of driver fatigue from camera input and provide timely feedback through a connected application.

The repository is organized as a multi-component system:

```text
Camera / Video
      │
      ▼
Python inference backend
      │
      ├── YOLOv8
      └── Vision Transformer (ViT)
      │
      ▼
Drowsiness result
      │
      ▼
React Native / Expo application

Next.js website
      └── Project presentation and information
```

## Repository structure

- `app/` — React Native / Expo mobile application
- `backend/` — Python inference service
- `website/` — Next.js project website
- `docs/` — project documentation
- `scripts/` — development setup and launch helpers

## Key capabilities

- Real-time camera-oriented drowsiness detection workflow
- YOLOv8-based visual detection
- Vision Transformer-based analysis
- Python inference service
- React Native / Expo mobile interface
- Next.js web presentation
- Modular separation between UI and inference components

## Backend

The inference service uses Python and includes:

- FastAPI
- Uvicorn
- OpenCV
- PyTorch
- Ultralytics YOLO
- ONNX Runtime
- NumPy / SciPy
- dlib
- python-dotenv

Install backend dependencies from `backend/requirements.txt`.

## Mobile application

The mobile client uses Expo and React Native with camera, navigation, notifications, gesture, animation, and visualization libraries.

From the `app/` directory:

```bash
npm install
npm start
```

Then choose the required Expo target.

## Development setup

The repository includes setup scripts, but they assume a Unix-like development environment. For a manual and portable setup:

```text
1. Create the Python environment in backend/
2. Install backend/requirements.txt
3. Install the app dependencies in app/
4. Install the website dependencies in website/ when its package manifest is present
5. Start each component independently
```

The application requires the model files and runtime configuration expected by the backend. Keep credentials and machine-specific configuration outside the repository.

## Engineering focus

NoNap demonstrates work across:

- Computer vision
- Deep learning inference
- Real-time application architecture
- REST / WebSocket-oriented backend services
- Mobile development
- Frontend development
- Model integration
- Modular project organization

## Status

Active academic project focused on building and evaluating a practical driver-drowsiness detection pipeline.

## Author / Repository

**Nikhil Kumar PE**

[GitHub](https://github.com/nikhilkumarpe-beep)

[Repository](https://github.com/nikhilkumarpe-beep/NoNap)
