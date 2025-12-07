from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import numpy as np
import cv2

app = FastAPI()

# Load model
model = YOLO("weights/best.pt")

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # Read image
    image_bytes = await file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Run inference
    results = model(img)

    # Convert detections into json
    detections = []
    for box in results[0].boxes:
        detections.append({
            "class": int(box.cls[0]),
            "confidence": float(box.conf[0]),
            "bbox": box.xyxy.tolist()
        })

    return JSONResponse(content={"detections": detections})
