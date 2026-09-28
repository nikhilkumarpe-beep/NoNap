"""WebSocket inference service for the NoNap driver-drowsiness prototype.

Run from the backend directory with: python -m uvicorn main:app --host 0.0.0.0 --port 8765
"""
import base64
import json
import logging
import time

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from pipeline.alert_engine import generate_alert_payload
from pipeline.clahe import enhance
from pipeline.detector import FaceDetector
from pipeline.ear_mar import calculate
from pipeline.hysteresis import HysteresisBuffer
from pipeline.vit_analyzer import ViTAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nonap")

app = FastAPI(title="NoNap Inference API", version="1.0.0")
detector = None
detector_error = None


@app.on_event("startup")
def load_models():
    global detector, detector_error
    try:
        detector = FaceDetector()
        detector_error = None
    except Exception as exc:
        detector_error = str(exc)
        logger.exception("Unable to initialize face detector")


@app.get("/health")
def health():
    return {
        "status": "ok" if detector is not None else "degraded",
        "detector_ready": detector is not None,
        "detector_error": detector_error,
        "fatigue_model": "EAR/MAR fallback (ViT weights not configured)",
    }


@app.websocket("/detection")
async def detection_socket(websocket: WebSocket):
    await websocket.accept()
    state_machine = HysteresisBuffer()
    analyzer = ViTAnalyzer()
    previous_frame_time = time.perf_counter()

    try:
        while True:
            message = await websocket.receive()
            if message.get("bytes") is not None:
                frame_bytes = message["bytes"]
            elif message.get("text") is not None:
                # The Expo client currently sends {"frame": "<base64>"} as JSON.
                try:
                    payload_in = json.loads(message["text"])
                    frame_bytes = base64.b64decode(payload_in["frame"], validate=True)
                except (ValueError, KeyError, TypeError, json.JSONDecodeError):
                    await websocket.send_json({"state": "UNKNOWN", "error": "Expected JPEG bytes or JSON with a base64 frame"})
                    continue
            else:
                continue

            encoded = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
            if frame is None:
                await websocket.send_json({"state": "UNKNOWN", "error": "Invalid image frame"})
                continue

            now = time.perf_counter()
            elapsed = now - previous_frame_time
            fps = 1.0 / elapsed if elapsed > 0 else 0.0
            previous_frame_time = now

            enhanced_frame, lighting = enhance(frame)
            if detector is None:
                await websocket.send_json({
                    "state": "UNKNOWN",
                    "error": "Face detector is not ready. Check /health and model setup.",
                    "ear": 0.0,
                    "mar": 0.0,
                    "bbox": [],
                    "landmarks": [],
                })
                continue

            detections = detector.detect(enhanced_frame)
            if not detections:
                await websocket.send_json({
                    "state": "UNKNOWN",
                    "ear": 0.0,
                    "mar": 0.0,
                    "fatigue_prob": 0.0,
                    "bbox": [],
                    "landmarks": [],
                    "lighting": lighting,
                    "fps": round(fps, 1),
                })
                continue

            face = max(detections, key=lambda item: item.confidence)
            ear, mar = calculate(face.landmarks_68)
            state = state_machine.update(ear, mar)
            fatigue_prob = analyzer.analyze(face.eye_roi, face.mouth_roi, ear, mar)
            fatigue_prob = analyzer.get_final_score(fatigue_prob, ear, mar)

            payload = generate_alert_payload(
                state=state,
                ear=ear,
                mar=mar,
                fatigue_prob=fatigue_prob,
                blink_count=state_machine.blink_count,
                yawn_count=state_machine.yawn_count,
                lighting=lighting,
                fps=fps,
                bbox=face.bounding_box,
                landmarks=face.landmarks_68,
            )
            await websocket.send_json(payload)
    except WebSocketDisconnect:
        logger.info("Detection client disconnected")
    except Exception:
        logger.exception("Detection WebSocket failed")
        try:
            await websocket.close(code=1011, reason="Inference error")
        except Exception:
            pass
