
# CivicVision — Road Defect & Litter Detection System

An end-to-end AI-powered solution for automated detection and classification of road defects and roadside waste. CivicVision integrates **YOLOv8** deep learning capabilities with a **FastAPI** backend, modern **HTML/CSS/JavaScript** frontend, and containerized **Docker** deployment for seamless production deployment.

## Detection Capabilities

The system detects and classifies three object categories:

- **Potholes** — Road surface defects and structural damage
- **Plastic Waste** — Single-use plastics and plastic materials
- **Roadside Litter** — General debris, refuse, and discarded items

## Core Features

- **Image Detection** — Process and analyze single images with annotated bounding boxes
- **Video Detection** — Frame-by-frame analysis with automatic deduplication
- **Real-time Counting** — Aggregate object counts by detection type
- **Adjustable Confidence** — Configurable detection thresholds (0.1–1.0)
- **Output Persistence** — Automatic saving of annotated results

## System Architecture

```
User (Browser)
    ↓
Frontend (HTML/CSS/JavaScript)
    ↓
FastAPI REST Backend
    ↓
YOLOv8 Model (models/road.pt)
    ↓
Detection Results (Annotated Images/Videos)
```

## Project Structure

```
Civicvision/
├── backend/
│   ├── main.py                        # FastAPI application & YOLOv8 inference
│   └── models/
│       └── road.pt                    # Trained YOLOv8 model (3 classes)
├── frontend/
│   ├── index.html                     # Web interface
│   ├── script.js                      # Frontend client logic
│   ├── style.css                      # Styling & responsive design
│   └── static/output/                 # Detection results storage
├── training/
│   ├── data.yaml                      # YOLO dataset configuration
│   └── finalroaddetection.ipynb       # Training notebook (Google Colab)
├── Dockerfile                          # Container configuration
├── requirements.txt                    # Python dependencies
└── README.md                           # Documentation
```

**Key Paths:**
- Backend API: `backend/main.py`
- Trained Model: `backend/models/road.pt`
- Web UI: `frontend/index.html`
- Output Directory: `frontend/static/output/`

## Model Architecture

The system utilizes a single unified **YOLOv8** model trained on three object classes:

| Class ID | Object Type | Bounding Box Color |
|:--------:|:------------|:------------------:|
| 0        | Pothole     | Blue               |
| 1        | Plastic Waste | Red               |
| 2        | Other Litter | Green              |

## Training & Model Development

Training conducted in Google Colab for reproducibility and GPU acceleration. The repository includes:

- **Notebook**: `training/finalroaddetection.ipynb` — Complete end-to-end training pipeline
- **Dataset Config**: `training/data.yaml` — YOLO format dataset specification

### Training Configuration
- **Framework**: Ultralytics YOLOv8
- **Task**: Object Detection
- **Epochs**: 50
- **Output Model**: `backend/models/road.pt`

## Quick Start — Local Development

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Start the backend server**
```bash
python backend/main.py
```

3. **Access the application**
```
http://localhost:8000
```

## Docker Deployment — Production

### Build and Run

```bash
# Build the image
docker build -t civicvision .

# Run container on port 8000
docker run -p 8000:8000 civicvision

# Access application
# Open: http://localhost:8000
```

### Run on Custom Port

```bash
# Run on alternate port (e.g., 9000)
docker run -p 9000:8000 civicvision
# Open: http://localhost:9000
```

## API Reference

### Detect Objects in Image

**Endpoint:** `POST /detect/image`

Processes a single image and returns detection results with object counts.

**Parameters:**

| Parameter | Type | Range | Description |
|:----------|:----:|:-----:|:------------|
| `file` | File | — | Image file (JPG, PNG) |
| `confidence` | Float | 0.1–1.0 | Detection confidence threshold |

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

### Detect Objects in Video

**Endpoint:** `POST /detect/video`

Processes video frames with automatic tracking deduplication.

**Parameters:**

| Parameter | Type | Range | Description |
|:----------|:----:|:-----:|:------------|
| `file` | File | — | Video file (MP4, MOV) |
| `confidence` | Float | 0.1–1.0 | Detection confidence threshold |

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

---

### Get Web Interface

**Endpoint:** `GET /`

Returns the frontend web application UI.

## Technology Stack

| Component | Technology | Purpose |
|:----------|:-----------|:--------|
| **ML Model** | YOLOv8 (Ultralytics) | Object detection & inference |
| **Backend** | FastAPI + Uvicorn | REST API server |
| **Frontend** | HTML5, CSS3, JavaScript | User interface & client logic |
| **Vision** | OpenCV | Image processing & annotation |
| **Video** | ImageIO + FFmpeg | Video encoding & frame processing |
| **Compute** | PyTorch + CUDA | GPU-accelerated inference |
| **Containerization** | Docker | Production deployment |
| **Runtime** | Python 3.10 | Application runtime environment |

## Performance Optimization

- **GPU Acceleration** — Enable CUDA for 3–5x faster inference (NVIDIA GPUs supported)
- **Confidence Threshold** — Use `confidence ≥ 0.4` to minimize false positives
- **Video Processing** — Reduce frame skip rate for faster batch processing
- **Disk Management** — Periodically clear `frontend/static/output/` for optimal storage
- **Model Optimization** — FP16 half-precision inference enabled for GPU deployment

## Troubleshooting

### Model File Not Found
**Error:** `FileNotFoundError: backend/models/road.pt`

**Solution:** Verify the model file exists:
```bash
ls -la backend/models/road.pt  # Linux/Mac
dir backend\models\road.pt     # Windows
```

---

### Port Already in Use
**Error:** `Address already in use: 0.0.0.0:8000`

**Solution:** Use an alternative port:
```bash
# Docker: Run on port 9000
docker run -p 9000:8000 civicvision

# Local: Modify main.py or use environment variable
```

---

### Docker Not Available
**Error:** `docker: command not found`

**Solution:** Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

## Project Status

| Component | Status | Notes |
|:----------|:------:|:------|
| YOLOv8 Model Training | ✅ Complete | 50 epochs, 3 object classes |
| Web Application | ✅ Complete | Image & video detection |
| Docker Deployment | ✅ Complete | Production-ready container |
| API Documentation | ✅ Complete | Full REST API specification |
| Demo Readiness | ✅ Complete | Ready for evaluation & deployment |

## License

This project utilizes **Ultralytics YOLOv8** under the AGPL-3.0 License. For commercial usage, refer to [Ultralytics Licensing](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) terms and requirements.

