
# CivicVision — Road Defect & Litter Detection (YOLOv8 + FastAPI)

CivicVision is an end-to-end, AI-powered web application for detecting road defects and roadside waste using a unified **YOLOv8** object detection model. It provides a **FastAPI** backend, a lightweight **HTML/CSS/JavaScript** frontend, and **Docker** support for simple deployment.

## What it detects

- Potholes
- Plastic waste
- Other roadside litter

## Key features

- Image detection
- Video detection
- Live webcam detection
- Real-time object counting
- Output saving for processed images/videos

## System architecture

```text
User (Browser)
	 ↓
Frontend (HTML/CSS/JS)
	 ↓
FastAPI Backend
	 ↓
YOLOv8 Model (models/road.pt)
	 ↓
Detection Results (Images / Videos)
```

## Project structure

```text
Civicvision/
├── backend/
│   ├── main.py                   # FastAPI backend with YOLOv8 inference
│   └── models/
│       └── road.pt               # Trained YOLOv8 model
├── frontend/
│   ├── index.html                # Web UI
│   ├── script.js                 # Frontend JavaScript logic
│   ├── style.css                 # Styling
│   └── static/
│       └── output/               # Saved detection results (images/videos)
├── training/
│   ├── data.yaml                 # YOLO dataset configuration
│   └── finalroaddetection.ipynb  # Google Colab training notebook
├── Dockerfile                    # Container configuration
├── requirements.txt              # Python dependencies
└── README.md
```

**Key paths:**
- Backend app: `backend/main.py`
- Model file: `backend/models/road.pt`
- Frontend UI: `frontend/index.html`
- Detection outputs: `frontend/static/output/`

## Model details

The system uses a single unified YOLOv8 model: `backend/models/road.pt`, trained on 3 classes.

| Class ID | Class name    |
|---------:|---------------|
| 0        | pothole       |
| 1        | plastic       |
| 2        | otherlitter   |

### Bounding box colors

- Blue → Pothole
- Red → Plastic
- Green → Other litter

## Training (included for reproducibility)

Training was performed in Google Colab. For transparency and reproducibility, this repository includes:

- `training/finalroaddetection.ipynb`
- `training/data.yaml`

Training summary:

- Framework: Ultralytics YOLOv8
- Task: Object Detection
- Epochs: 50
- Output: `road.pt`

## Run locally (without Docker)

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Start the backend

```bash
python backend/main.py
```

### 3) Open the app

- http://localhost:8000

## Docker deployment (recommended)

### 1) Build the image

```bash
docker build -t civicvision .
```

### 2) Run the container

```bash
docker run -p 8000:8000 civicvision
```

### 3) Open in browser

- http://localhost:8000

## API endpoints

### `GET /`

Returns the frontend UI.

### `POST /detect/image`

**Inputs**

- `file` (image)
- `confidence` (float, 0.1–1.0)

**Returns (example)**

```json
{
	"image_url": "/static/output/result.jpg",
	"counts": {
		"pothole": 2,
		"plastic": 1,
		"otherlitter": 3
	}
}
```

### `POST /detect/video`

**Inputs**

- `file` (video)
- `confidence` (float, 0.1–1.0)

**Returns (example)**

```json
{
	"video_url": "/static/output/result.mp4",
	"counts": {
		"pothole": 5,
		"plastic": 2,
		"otherlitter": 4
	}
}
```

## Tech stack

| Layer      | Technology            |
|------------|------------------------|
| Model      | YOLOv8 (Ultralytics)   |
| Backend    | FastAPI                |
| Frontend   | HTML, CSS, JavaScript  |
| CV         | OpenCV                 |
| Video      | FFmpeg, ImageIO        |
| Deployment | Docker                 |
| Training   | Google Colab           |
| Language   | Python                 |

## Performance tips

- GPU improves inference speed (CUDA supported).
- Use confidence ≥ 0.4 to reduce false positives.
- Lower FPS for faster video processing.
- Clear `frontend/static/output/` occasionally to free disk space.

## Troubleshooting

### Model not found

Confirm the file exists:

- `backend/models/road.pt`

### Port already in use

Run on a different host port:

```bash
docker run -p 9000:8000 civicvision
```

Then open:

- http://localhost:9000

### Docker not found

Make sure Docker Desktop is installed and running.

## Hackathon pitch line

"We built an end-to-end AI system using YOLOv8, FastAPI, and Docker to automatically detect potholes and roadside waste from images, videos, and live cameras."

## License

This project uses Ultralytics YOLO. Please refer to Ultralytics licensing terms for commercial usage.

## Status

| Component        | Status |
|------------------|--------|
| Model training   | Done   |
| Web app          | Done   |
| Docker deployment| Done   |
| Demo-ready       | Yes    |

