
# CivicVision — Road Defect & Litter Detection System

CivicVision is an end-to-end AI-powered web application for automated detection of road defects and roadside waste using **YOLOv8** deep learning model. The system combines a **FastAPI** backend, responsive **HTML/CSS/JavaScript** frontend, and containerized **Docker** deployment for production-ready infrastructure monitoring.

## Detection Capabilities

The system detects and classifies three object categories:
- **Potholes** — Road surface defects
- **Plastic waste** — Discarded plastic materials
- **Roadside litter** — General debris and refuse

## Core Features

✓ **Image Detection** — Process single images with annotated bounding boxes  
✓ **Video Detection** — Frame-by-frame analysis with automatic deduplication  
✓ **Real-time Counting** — Aggregate object counts per detection type  
✓ **Adjustable Confidence** — Configurable detection thresholds (0.1–1.0)  
✓ **Output Persistence** — Automatic saving of annotated results

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

## Model Architecture

The system utilizes a single unified **YOLOv8** model trained on three object classes:

| Class ID | Object Type     | Detection Color |
|:--------:|-----------------|:---------------:|
| 0        | Pothole         | Blue            |
| 1        | Plastic Waste   | Red             |
| 2        | Other Litter    | Green           |

## Training & Model Development

Training was conducted in Google Colab for reproducibility. Repository includes:
- **Notebook**: `training/finalroaddetection.ipynb` — Complete training pipeline
- **Dataset Config**: `training/data.yaml` — YOLO format dataset specification

**Training Configuration:**
- Framework: Ultralytics YOLOv8
- Task: Object Detection
- Epochs: 50
- Output Model: `backend/models/road.pt`

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- pip package manager

### Installation & Execution

```bash
pip install -r requirements.txt
```

### 2) Start the backend

```bash
python backend/main.py
```

### 3) Open the app

- http://localhost:8000

## Docker Deployment (Production)

### Build & Run

```bash
docker build -t civicvision .

# Run container on port 8000
docker run -p 8000:8000 civicvision

# Access application
# Open: http://localhost:8000
```

### Custom Port

```bash
# Run on alternate port (e.g., 8000)
docker run -p 8000:8000 civicvision
# Open: http://localhost:9000
```

## API Reference

### `GET /`
Returns the web application frontend UI.

---

### `POST /detect/image`
Detect objects in a single image.

**Request Parameters:**
| Parameter    | Type  | Range    | Description              |
|:-------------|:-----:|:--------:|-------------------------|
| `file`       | File  | —        | Image file (JPG, PNG)    |
| `confidence` | Float | 0.1–1.0  | Detection confidence    |

**Response Example:**
```json
{
  "image_url": "/static/output/abc123.jpg",
  "counts": {
    "pothole": 2,
    "plastic": 1,
    "otherlitter": 3
  }
}
```

---

### `POST /detect/video`
Detect objects across all video frames with automatic tracking deduplication.

**Request Parameters:**
| Parameter    | Type  | Range    | Description               |
|:-------------|:-----:|:--------:|---------------------------|
| `file`       | File  | —        | Video file (MP4, MOV)     |
| `confidence` | Float | 0.1–1.0  | Detection confidence     |

**Response Example:**
```json
{
  "video_url": "/static/output/xyz789.mp4",
  "counts": {
    "pothole": 5,
    "plastic": 2,
    "otherlitter": 4
  }
}
```

## Technology Stack

| Layer        | Technology              | Purpose                        |
|:-------------|:------------------------|:-------------------------------|
| **ML Model** | YOLOv8 (Ultralytics)   | Object detection & inference   |
| **Backend**  | FastAPI + Uvicorn      | REST API server                |
| **Frontend** | HTML5, CSS3, JavaScript | User interface                 |
| **Vision**   | OpenCV                 | Image processing & annotation  |
| **Video**    | ImageIO + FFmpeg       | Video encoding & processing    |
| **GPU**      | PyTorch + CUDA         | Accelerated inference          |
| **Container**| Docker                 | Containerization & deployment  |
| **Runtime**  | Python 3.10            | Application runtime            |

## Performance Optimization

- **GPU Acceleration** — Enable CUDA for 3–5x faster inference (supported)
- **Confidence Threshold** — Use `confidence ≥ 0.4` to minimize false positives
- **Video Processing** — Reduce frame skip rate for faster batch processing
- **Disk Management** — Periodically clear `frontend/static/output/` to maintain disk space
- **Model Optimization** — FP16 half-precision enabled for GPU inference

## Troubleshooting

### ✗ Model File Not Found
**Error:** `FileNotFoundError: backend/models/road.pt`  
**Solution:** Verify model file exists:
```bash
ls -la backend/models/road.pt  # Linux/Mac
dir backend\models\road.pt     # Windows
```

### ✗ Port Already in Use
**Error:** `Address already in use: 0.0.0.0:8000`  
**Solution:** Use alternative port:
```bash
# Docker: Run on port 9000
docker run -p 9000:8000 civicvision

# Local: Modify main.py or use environment variable
```

### ✗ Docker Not Available
**Error:** `docker: command not found`  
**Solution:** Install Docker Desktop from https://www.docker.com/products/docker-desktop

## Project Status

| Component              | Status      | Notes                    |
|:-----------------------|:-----------:|:------------------------:|
| YOLOv8 Model Training  | ✅ Complete | 50 epochs, 3 classes    |
| Web Application        | ✅ Complete | Image & video detection |
| Docker Deployment      | ✅ Complete | Production-ready        |
| API Documentation      | ✅ Complete | Full REST specification |
| Demo Readiness         | ✅ Complete | Ready for evaluation    |

## License

This project uses **Ultralytics YOLOv8** under AGPL-3.0 License. For commercial usage, please refer to [Ultralytics Licensing](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) terms and requirements.

