# Testing Documentation

## Overview

This document provides comprehensive instructions for executing automated tests on the Road Defect Detection System within a Docker containerized environment. The testing suite validates the YOLO model's performance on both static images and video streams.

---

## Prerequisites

### Directory Structure

Ensure the following directory structure is present in your project:

```
Tests/
 └── data/
     ├── images/          # Test image files
     ├── videos/          # Test video files
     └── run_test.py      # Automated test script
```

### Test Asset Organization

| Asset Type | Location | Description |
|------------|----------|-------------|
| Test Images | `Tests/data/images/` | Static images for detection validation |
| Test Videos | `Tests/data/videos/` | Video files for temporal detection testing |
| Test Script | `Tests/data/run_test.py` | Automated test execution script |

---

## Testing Procedure

### Step 1: Build Docker Image

Navigate to the project root directory and execute:

```bash
docker build -t civicvision .
```

### Step 2: Initialize Container

Launch the Docker container with port mapping:

```bash
docker run -d -p 8000:8000 --name cranky_feynman civicvision
```

**Parameters:**
- `-d`: Run container in detached mode
- `-p 8000:8000`: Map port 8000 from container to host
- `--name`: Assign container identifier

### Step 3: Access Container Shell

Enter the running container:

```bash
docker exec -it cranky_feynman bash
```

### Step 4: Navigate to Application Root

```bash
cd /app
```

### Step 5: Verify Test Assets

Confirm test data availability:

```bash
ls Tests/data/images
ls Tests/data/videos
```

**Expected Result:** Display of uploaded test files in respective directories.

### Step 6: Execute Test Suite

Run the automated test script:

```bash
python Tests/data/run_test.py
```

---

## Test Results Interpretation

### Sample Output

```
=== IMAGE TESTS ===
[DETECTED] pothole.jpg → ['pothole']
[NO DETECTION] cleanroad.jpg

=== VIDEO TESTS ===
[DETECTED] garbage.mp4 → ['plastic', 'otherlitter']
[NO DETECTION] indoor.mp4
```

### Output Legend

| Status | Description |
|--------|-------------|
| `[DETECTED]` | Model successfully identified one or more objects in the asset |
| `[NO DETECTION]` | No objects detected; asset contains no defects or is out of scope |

### Detected Objects

When objects are detected, the output displays a list of identified defect classes (e.g., `['pothole']`, `['plastic', 'otherlitter']`).

---

## Purpose

This testing framework enables:

- **Model Validation**: Verify YOLO model accuracy on diverse inputs
- **Regression Testing**: Ensure model performance consistency across updates
- **Docker Environment Testing**: Validate deployment configuration and dependencies
- **Batch Processing**: Test multiple assets efficiently via command-line interface

---

## Troubleshooting

### Common Issues

**Container not found:**
- Verify container name matches the one created in Step 2
- Check running containers: `docker ps -a`

**Test files not visible:**
- Ensure files are properly copied during Docker build process
- Verify Dockerfile COPY instructions include test directories

**Script execution errors:**
- Confirm Python dependencies are installed in container
- Check model file (`backend/models/road.pt`) is present

---

## Additional Resources

For more information on model training and deployment, refer to:
- [README.md](README.md) - Project overview and setup
- [training/roaddetectionfinal.ipynb](training/roaddetectionfinal.ipynb) - Model training documentation