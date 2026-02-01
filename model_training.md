# Model Training Documentation

## Overview

This document provides documentation of the training process for the YOLO-based Road Defect Detection System, as implemented in the training notebook.

---

## Dataset Setup

### Dataset Extraction

The dataset is extracted from a compressed archive:

```bash
!unzip finaldataedited.zip -d FINALDATA
```

### Directory Structure

```
FINALDATA/
 └── finaldataedited/
     ├── images/
     │   ├── train/          # Training images
     │   └── val/            # Validation images
     ├── labels/
     │   ├── train/          # Training annotations (.txt)
     │   └── val/            # Validation annotations (.txt)
     └── data.yaml           # Dataset configuration
```

### Dataset Verification

File counts can be verified using:

```bash
!ls FINALDATA/finaldataedited/images/train | wc -l
!ls FINALDATA/finaldataedited/labels/train | wc -l
```

---

## Detection Classes

The model is trained to detect three classes of road defects and environmental hazards:

| Class ID | Class Name | Description |
|----------|------------|-------------|
| 0 | `pothole` | Road surface depressions and structural defects |
| 1 | `plastic` | Plastic waste and debris |
| 2 | `otherlitter` | General litter and non-plastic waste materials |

These classes are defined in the `data.yaml` configuration file located at `FINALDATA/data.yaml`.

---

## Environment Setup

### Dependencies Installation

```bash
!pip install ultralytics
```

### Library Import

```python
from ultralytics import YOLO
```

---

## Training Configuration

### Model Initialization

```python
model = YOLO("yolov8n.pt")
```

**Base Model**: YOLOv8 Nano (`yolov8n.pt`)

### Training Execution

```python
model.train(
    data="FINALDATA/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16
)
```

### Training Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Model** | `yolov8n.pt` | Pre-trained YOLOv8 Nano weights |
| **Data** | `FINALDATA/data.yaml` | Dataset configuration file |
| **Epochs** | 50 | Training iterations through dataset |
| **Image Size** | 640 | Input image resolution (pixels) |
| **Batch Size** | 16 | Images per training batch |

---

## Model Output

### Trained Weights Location

After training completion, the model weights are saved to:

```
runs/detect/train2/weights/
```

The directory contains:
- `best.pt` - Best performing checkpoint
- `last.pt` - Final epoch checkpoint

### Verification

```bash
!ls runs/detect/train2/weights
```

---

## Model Validation

### Validation Execution

```python
from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")
model.val(data="FINALDATA/data.yaml")
```

The validation evaluates the trained model against the validation dataset defined in `data.yaml`.

---

## Model Inference

### Batch Prediction (Validation Set)

```python
model.predict(
    source="FINALDATA/finaldataedited/images/val",
    conf=0.4,
    save=True
)
```

**Parameters:**
- `source`: Path to validation images
- `conf`: Confidence threshold (0.4 = 40%)
- `save`: Save annotated output images

### Single Image Prediction

```python
model.predict("/content/images (1).jpeg", conf=0.4, save=True)
```

Tests model inference on individual images with 40% confidence threshold.

---

## Deployment

### Production Model

The trained model (`best.pt`) is deployed as:

**Location**: `backend/models/road.pt`

**Integration**: Loaded by FastAPI backend for real-time inference on uploaded images and videos.

---

## Training Workflow Summary

1. **Extract Dataset**: Unzip training data to `FINALDATA/` directory
2. **Verify Data**: Count images and labels to ensure proper extraction
3. **Install Dependencies**: Install Ultralytics YOLO library
4. **Initialize Model**: Load YOLOv8 Nano pre-trained weights
5. **Train Model**: Execute 50-epoch training with specified parameters
6. **Verify Output**: Check weights directory for trained model files
7. **Validate Model**: Run validation on test dataset
8. **Test Inference**: Perform predictions on validation images
9. **Deploy Model**: Copy `best.pt` to production location as `road.pt`

---

## References

- **Ultralytics YOLOv8**: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
- **Training Notebook**: [training/roaddetectionfinal.ipynb](training/roaddetectionfinal.ipynb)