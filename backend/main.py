from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from ultralytics import YOLO
import cv2

app = FastAPI()

# Load helmet-only model
model = YOLO("weights/helmet.pt")  # class: helmet only


def generate_frames():
    # GANTI 1 → untuk webcam eksternal (biasanya benar)
    cap = cv2.VideoCapture(0)   # kalau tidak muncul, coba 0 atau 2

    if not cap.isOpened():
        print("❌ Webcam tidak ditemukan!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        # YOLO inference
        results = model(frame)
        annotated = results[0].plot()  # gambar hasil dengan bounding box

        # Encode JPG
        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        # Streaming ke browser (MJPEG stream)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


@app.get("/video")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
