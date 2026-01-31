from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import cv2, uuid, os
import numpy as np
from ultralytics import YOLO
import imageio

# Force CPU (Railway has no GPU)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

app = FastAPI(title="Road Defect Detection System")

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
MODEL_PATH = os.path.join(BASE_DIR, "models/road.pt")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- SERVE FRONTEND ----------------
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Serve outputs
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# ---------------- LOAD MODEL ----------------
print("Loading model on CPU...")
model = YOLO(MODEL_PATH)
model.to("cpu")
print("Model loaded.")

# ---------------- IMAGE DETECTION ----------------
def detect_frame(frame, conf):
    result = model(frame, conf=conf)[0]
    counts = {"pothole": 0, "plastic": 0, "otherlitter": 0}
    annotated = result.plot()

    for box in result.boxes:
        cls = int(box.cls[0])
        name = model.names[cls].lower()
        if name in counts:
            counts[name] += 1
        else:
            counts["otherlitter"] += 1

    return annotated, counts

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...), conf: float = 0.5):
    try:
        img = np.frombuffer(await file.read(), np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Invalid image file")
        img = cv2.resize(img, (640, 640))
        annotated, counts = detect_frame(img, conf)

        out_name = f"{uuid.uuid4().hex}.jpg"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        cv2.imwrite(out_path, annotated)

        return {
            "image_url": "/outputs/" + out_name,
            "counts": counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- VIDEO DETECTION (NO DUPLICATES) ----------------
@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...), conf: float = 0.5):
    try:
        temp = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}_in.mp4")
        with open(temp, "wb") as f:
            f.write(await file.read())

        reader = imageio.get_reader(temp)
        fps = reader.get_meta_data().get('fps', 30)

        out_name = f"{uuid.uuid4().hex}.mp4"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        writer = imageio.get_writer(out_path, fps=fps)

        seen_potholes = set()
        seen_plastic = set()
        seen_litter = set()

        frame_skip = 1  # IMPORTANT for free tier

        for i, frame in enumerate(reader):
            if i % frame_skip != 0:
                continue

            original = frame.copy()                # keep original size
            resized = cv2.resize(frame, (640, 640))

            result = model.track(resized, conf=conf, persist=True)[0]

            for box in result.boxes:
                if box.id is None:
                    continue

                cls = int(box.cls[0])
                name = model.names[cls].lower()

                # scale boxes back to original size
                x1, y1, x2, y2 = box.xyxy[0]
                h, w, _ = original.shape

                x1 = int(x1 * w / 640)
                x2 = int(x2 * w / 640)
                y1 = int(y1 * h / 640)
                y2 = int(y2 * h / 640)

                cv2.rectangle(original, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(original, name, (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # unique counting
                if name == "pothole":
                    seen_potholes.add(int(box.id[0]))
                elif name == "plastic":
                    seen_plastic.add(int(box.id[0]))
                else:
                    seen_litter.add(int(box.id[0]))

            writer.append_data(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
        writer.close()
        reader.close()
        os.remove(temp)

        return {
            "video_url": "/outputs/" + out_name,
            "counts": {
                "pothole": len(seen_potholes),
                "plastic": len(seen_plastic),
                "otherlitter": len(seen_litter)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
