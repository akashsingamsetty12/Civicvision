import os
import cv2
from ultralytics import YOLO

MODEL_PATH = "backend/models/road.pt"
DATA_DIR = "Tests/data"

model = YOLO(MODEL_PATH)

print("\n=== IMAGE TESTS ===")
image_dir = os.path.join(DATA_DIR, "images")

for img_name in os.listdir(image_dir):
    img_path = os.path.join(image_dir, img_name)
    img = cv2.imread(img_path)

    result = model(img)[0]
    detected = [model.names[int(b.cls[0])] for b in result.boxes]

    if detected:
        print(f"[DETECTED] {img_name} → {detected}")
    else:
        print(f"[NO DETECTION] {img_name}")

print("\n=== VIDEO TESTS ===")
video_dir = os.path.join(DATA_DIR, "videos")

for vid_name in os.listdir(video_dir):
    vid_path = os.path.join(video_dir, vid_name)

    result = model(vid_path, stream=True)
    detected = set()

    for frame in result:
        for b in frame.boxes:
            detected.add(model.names[int(b.cls[0])])

    if detected:
        print(f"[DETECTED] {vid_name} → {list(detected)}")
    else:
        print(f"[NO DETECTION] {vid_name}")
