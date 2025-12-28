from ultralytics import YOLO

model = YOLO("helmet.pt")

metrics = model.val(
    data="dataset/dataset.yaml",
    imgsz=640,
    device="cpu"
)

print(metrics)
