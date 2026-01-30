import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import tempfile
import torch
import os
import uuid
import imageio

st.markdown("""
<style>

/* Background */
.stApp {
    background: #f6f7fb;
}

/* Header title */
h1 {
    font-size: 32px;
    font-weight: 800;
    color: #4f46e5;
}

/* Tabs */
div[data-testid="stTabs"] button {
    font-size: 16px;
    font-weight: 600;
    color: #6b7280;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #4f46e5;
    border-bottom: 3px solid #4f46e5;
}

/* Buttons */
button[kind="primary"] {
    width: 100%;
    border-radius: 14px;
    background: linear-gradient(90deg, #6a7cff, #7b4fa3);
    color: white;
    font-size: 18px;
    font-weight: 700;
}

/* Upload box */
div[data-testid="stFileUploader"] {
    border: 2px dashed #4f46e5;
    border-radius: 16px;
    padding: 25px;
    background: white;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(180deg, #f8fafc, #eef2f7);
    padding: 16px;
    border-radius: 14px;
}

/* Images & video */
img, video {
    border-radius: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

/* Hide Streamlit junk */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Road Defect Detection", layout="wide")
st.title("🚧 Road Defect Detection System")

# ---------------- DEVICE ----------------
device = "cuda" if torch.cuda.is_available() else "cpu"
st.write("Using device:", device)

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    model = YOLO("models/road.pt")
    model.to(device)
    model.fuse()
    return model

road_model = load_model()

# ---------------- UTILS ----------------
color_map = {
    "pothole": (255, 0, 0),
    "plastic": (0, 0, 255),
    "otherlitter": (0, 255, 0)
}

def detect(image, conf):
    image = cv2.resize(image, (640, 640))
    counts = {"pothole": 0, "plastic": 0, "otherlitter": 0}

    result = road_model(image, conf=conf)[0]
    class_names = road_model.names

    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        c = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = class_names[class_id].lower()

        category = class_name if class_name in counts else "otherlitter"
        counts[category] += 1

        color = color_map.get(category, (255,255,255))
        cv2.rectangle(image,(x1,y1),(x2,y2),color,2)
        cv2.putText(image,f"{category} {c:.2f}",
                    (x1,y1-5),cv2.FONT_HERSHEY_SIMPLEX,0.6,color,2)

    return image, counts

# ---------------- UI ----------------
tab1, tab2 = st.tabs(["🖼 Image", "🎥 Video"])

# IMAGE TAB
with tab1:
    st.subheader("Upload Image")
    img_file = st.file_uploader("Choose image", type=["jpg","png","jpeg"])
    conf = st.slider("Confidence",0.1,1.0,0.5)

    if img_file:
        img = Image.open(img_file).convert("RGB")
        img = np.array(img)

        if st.button("Detect Image"):
            with st.spinner("Detecting..."):
                annotated, counts = detect(img, conf)
                st.image(annotated, channels="BGR")
                st.json(counts)

# VIDEO TAB
with tab2:
    st.subheader("Upload Video")
    vid_file = st.file_uploader("Choose video", type=["mp4","mov","avi"])
    conf = st.slider("Confidence",0.1,1.0,0.5, key="vconf")

    if vid_file:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(vid_file.read())

        if st.button("Detect Video"):
            with st.spinner("Processing video..."):
                reader = imageio.get_reader(tmp.name)
                fps = reader.get_meta_data().get('fps',30)
                out_path = f"outputs/{uuid.uuid4().hex}.mp4"
                os.makedirs("outputs", exist_ok=True)

                writer = imageio.get_writer(out_path, fps=fps)

                counts = {"pothole":0,"plastic":0,"otherlitter":0}

                for frame in reader:
                    frame = cv2.resize(frame,(640,480))
                    result = road_model(frame, conf=conf)[0]
                    annotated = result.plot()
                    writer.append_data(cv2.cvtColor(annotated,cv2.COLOR_BGR2RGB))

                    for box in result.boxes:
                        cls = int(box.cls[0])
                        name = road_model.names[cls].lower()
                        if name in counts:
                            counts[name]+=1

                writer.close()
                reader.close()

                st.video(out_path)
                st.json(counts)
