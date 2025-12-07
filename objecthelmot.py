from ultralytics import YOLO
import cv2
import torch

# Use GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load models
helmet_model = YOLO("best.pt")       # custom helmet model
coco_model = YOLO("yolov8n.pt")      # pretrained COCO model

# Helper function: compute IoU between two boxes
def box_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
    boxBArea = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])
    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return iou

# Open webcam/video
cap = cv2.VideoCapture('http://10.1.35.144:8080/video')  # 0 = default webcam, replace with video path if needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run predictions
    helmet_results = helmet_model.predict(frame, device=device, conf=0.5, verbose=False)
    coco_results = coco_model.predict(frame, device=device, conf=0.5, verbose=False)

    # Extract boxes
    persons = []
    motorcycles = []
    helmets = []

    for box in coco_results[0].boxes:
        cls_id = int(box.cls[0])
        label = coco_results[0].names[cls_id]
        coords = box.xyxy[0].tolist()
        if label == "person":
            persons.append(coords)
        elif label == "motorcycle":
            motorcycles.append(coords)

    for box in helmet_results[0].boxes:
        coords = box.xyxy[0].tolist()
        helmets.append(coords)

    # Counters
    with_helmet = 0
    without_helmet = 0

    # Draw boxes and check helmet
    for p_box in persons:
        riding = any(box_iou(p_box, m_box) > 0.3 for m_box in motorcycles)
        if riding:
            helmet_on = any(box_iou(p_box, h_box) > 0.1 for h_box in helmets)
            x1, y1, x2, y2 = map(int, p_box)
            if helmet_on:
                with_helmet += 1
                color = (0, 255, 0)  # green
                label_text = "Helmet"
            else:
                without_helmet += 1
                color = (0, 0, 255)  # red
                label_text = "No Helmet"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Display counts
    cv2.putText(frame, f"With Helmet: {with_helmet}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f"Without Helmet: {without_helmet}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Show frame
    cv2.imshow("Traffic Helmet Detection", frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
