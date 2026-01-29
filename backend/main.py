from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import tempfile
import torch
import os
import uuid
import imageio

app = FastAPI(title="Road Defect Detection System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directory exists before mounting
os.makedirs("/tmp/output", exist_ok=True)

# Serve model outputs at /static/output/<file>
app.mount(
    "/static/output",
    StaticFiles(directory="/tmp/output"),
    name="output",
)

# Serve frontend assets (style.css, script.js) at /static/<file>
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ---------------- DEVICE ----------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Enable GPU memory optimization
if device == "cuda":
    torch.cuda.set_per_process_memory_fraction(0.9)
    torch.cuda.empty_cache()

# ---------------- MODELS ----------------
# Load model with FP16 half precision for faster inference
road_model = YOLO("backend/models/road.pt")
road_model.to(device)

# Enable inference optimization
road_model.fuse()  # Fuse conv+bn layers for speed
if device == "cuda":
    road_model.half()  # Use FP16 for faster inference on GPU

# Class name mapping (adjust based on your road.pt model's class names)
class_mapping = {
    "pothole": "pothole",
    "plastic": "plastic",
    "litter": "otherlitter",
    "otherlitter": "otherlitter",
    "trash": "otherlitter"
}

# Color mapping for visualization
color_map = {
    "pothole": (255, 0, 0),      # Blue
    "plastic": (0, 0, 255),      # Red
    "otherlitter": (0, 255, 0)   # Green
}

# Create output directory
output_dir = "/tmp/output"
os.makedirs(output_dir, exist_ok=True)

# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("frontend/index.html")

# ---------------- INFERENCE ----------------
def calculate_iou(box1, box2):
    """Calculate Intersection over Union (IoU) between two boxes"""
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    
    # Calculate intersection area
    inter_xmin = max(x1_min, x2_min)
    inter_ymin = max(y1_min, y2_min)
    inter_xmax = min(x1_max, x2_max)
    inter_ymax = min(y1_max, y2_max)
    
    if inter_xmax < inter_xmin or inter_ymax < inter_ymin:
        return 0.0
    
    inter_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)
    
    # Calculate union area
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area if union_area > 0 else 0.0

def deduplicate_detections(boxes_data, iou_threshold=0.3):
    """Remove duplicate detections with same class and overlapping boxes"""
    if not boxes_data:
        return []
    
    # Sort by confidence score (descending)
    sorted_boxes = sorted(boxes_data, key=lambda x: x['conf'], reverse=True)
    keep_boxes = []
    
    for i, box_data in enumerate(sorted_boxes):
        is_duplicate = False
        
        # Check against already kept boxes
        for kept_box in keep_boxes:
            # Only check if same category
            if kept_box['category'] == box_data['category']:
                iou = calculate_iou(
                    (box_data['x1'], box_data['y1'], box_data['x2'], box_data['y2']),
                    (kept_box['x1'], kept_box['y1'], kept_box['x2'], kept_box['y2'])
                )
                # If IoU is high and same class, it's a duplicate
                if iou > iou_threshold:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            keep_boxes.append(box_data)
    
    return keep_boxes

def detect(image, conf):
    image = cv2.resize(image, (640, 640))
    
    counts = {"pothole": 0, "plastic": 0, "otherlitter": 0}
    
    # Use agnostic NMS and faster processing
    result = road_model(image, conf=conf, imgsz=640, verbose=False)[0]
    
    # Get class names from the model
    class_names = road_model.names  # Returns dict of {class_id: class_name}
    
    # Collect all detections first
    boxes_data = []
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        c = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = class_names.get(class_id, "unknown")
        
        # Map detected class to our category
        category = class_mapping.get(class_name.lower(), "otherlitter")
        
        boxes_data.append({
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'conf': c,
            'class_name': class_name,
            'category': category
        })
    
    # Remove duplicate detections with higher threshold for speed
    unique_boxes = deduplicate_detections(boxes_data, iou_threshold=0.4)
    
    # Draw unique detections and count
    for box_data in unique_boxes:
        x1, y1, x2, y2 = box_data['x1'], box_data['y1'], box_data['x2'], box_data['y2']
        c = box_data['conf']
        category = box_data['category']
        
        counts[category] += 1
        
        # Get color for this category
        color = color_map.get(category, (128, 128, 128))
        
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, f"{category} {c:.2f}",
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return image, counts

# ---------------- IMAGE ----------------
@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...), confidence: float = 0.5):
    img = Image.open(file.file).convert("RGB")
    img = np.array(img)

    annotated, counts = detect(img, confidence)

    os.makedirs("/tmp/output", exist_ok=True)
    name = f"{uuid.uuid4().hex}.jpg"
    path = f"/tmp/output/{name}"
    cv2.imwrite(path, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))

    return {
        "image_url": f"https://civicvision.onrender.com/static/output/{name}",
        "counts": counts
    }

# ---------------- VIDEO ----------------
@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...), confidence: float = 0.5):
    """
    Process video frames with detection and save as MP4 using imageio
    Ensures all frames have consistent dimensions
    """
    seen_potholes = set()
    seen_plastic = set()
    seen_litter = set()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tmp.write(await file.read())
    tmp.close()

    try:
        # Read video with imageio
        reader = imageio.get_reader(tmp.name)
        fps = reader.get_meta_data().get('fps', 30)
        
        output_dir = "/tmp/output"
        os.makedirs(output_dir, exist_ok=True)
        
        final_output = f"{output_dir}/{uuid.uuid4().hex}.mp4"
        
        # Target frame size (must be divisible by 16 for codec compatibility)
        target_width = 640
        target_height = 368  # Divisible by 16 for H.264 codec
        
        total = {"pothole": 0, "plastic": 0, "otherlitter": 0}
        frame_count = 0
        frame_skip = 2
        
        print(f"✅ Processing video at {fps} FPS")
        print(f"✅ Target frame size: {target_width}x{target_height}")

        # Collect all frames first
        all_frames = []
        
        for frame_idx, frame in enumerate(reader):
            frame_count += 1
            
            # Ensure frame is resized to exactly target size
            frame = cv2.resize(frame, (target_width, target_height))
            
            # Verify frame is RGB
            if len(frame.shape) != 3 or frame.shape[2] not in [3, 4]:
                print(f"⚠️  Warning: Frame {frame_idx} has unexpected shape: {frame.shape}")
                continue
            
            # Process every frame_skip-th frame for detection
            if frame_count % frame_skip == 0:
                # Convert to BGR for detect function if needed
                if frame.shape[2] == 4:  # RGBA
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
                elif frame.shape[2] == 3:  # RGB
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                else:
                    frame_bgr = frame
                
                result = road_model.track(frame_bgr, conf=confidence, persist=True)[0]
                annotated = result.plot()
                class_names = road_model.names

                for box in result.boxes:
                    if box.id is None:
                        continue
                    obj_id = int(box.id[0])
                    class_id = int(box.cls[0])
                    class_name = class_names[class_id]

                    if class_name == "pothole":
                        seen_potholes.add(obj_id)
                    elif class_name == "plastic":
                        seen_plastic.add(obj_id)
                    else:
                        seen_litter.add(obj_id)
                
                # Ensure annotated frame is resized to target dimensions
                annotated = cv2.resize(annotated, (target_width, target_height))
                
                # Convert to RGB for imageio output
                output_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            else:
                # Keep unprocessed frame as RGB
                if frame.shape[2] == 4:  # RGBA
                    output_frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                elif frame.shape[2] == 3:  # RGB
                    output_frame = frame
                else:
                    output_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    output_frame = cv2.cvtColor(output_frame, cv2.COLOR_BGR2RGB)
            
            # Final verification of frame size before adding
            if output_frame.shape[0] != target_height or output_frame.shape[1] != target_width:
                print(f"⚠️  Resizing frame {frame_idx} from {output_frame.shape} to target {target_height}x{target_width}")
                output_frame = cv2.resize(output_frame, (target_width, target_height))
            
            all_frames.append(output_frame.astype('uint8'))
        
        reader.close()
        
        print(f"✅ Processed {len(all_frames)} frames")
        print(f"✅ Verifying all frames are {target_width}x{target_height}...")
        
        # Verify all frames have same dimensions
        for i, frame in enumerate(all_frames):
            if frame.shape != (target_height, target_width, 3):
                print(f"❌ Frame {i} has wrong shape: {frame.shape}, expected ({target_height}, {target_width}, 3)")
                # Force correct dimensions
                all_frames[i] = cv2.resize(frame, (target_width, target_height))
        
        print(f"✅ Now encoding {len(all_frames)} frames to MP4...")
        
        # Write all frames to MP4 with verified dimensions
        writer = imageio.get_writer(final_output, fps=fps, codec='libx264', pixelformat='yuv420p')
        for idx, frame in enumerate(all_frames):
            try:
                writer.append_data(frame)
            except Exception as e:
                print(f"❌ Error writing frame {idx}: {e}")
                raise
        writer.close()
        
        print(f"✅ Video saved successfully to: {final_output}")
        
        os.remove(tmp.name)
        return {
            "video_url": f"https://civicvision.onrender.com/static/output/{os.path.basename(final_output)}?t={uuid.uuid4().hex}",
            "counts": {
                "pothole": len(seen_potholes),
                "plastic": len(seen_plastic),
                "otherlitter": len(seen_litter)
            }
        }

    except Exception as e:
        print(f"❌ Video error: {str(e)}")
        import traceback
        traceback.print_exc()
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
