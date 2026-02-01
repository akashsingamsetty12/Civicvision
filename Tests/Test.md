# ROAD DEFECT DETECTION SYSTEM

# Image & Video Testing Report

# Positive Image Test 1 - Pothole

**Test Type**: Positive Image

**Input**: Image of a clear road pothole

**Expected**: Pothole should be detected

**Actual**: Pothole detected with bounding box

**Result:**Pass

## Observation:

The model correctly identified the pothole with high confidence and accurate localization.

**Input image:**


![](https://web-api.textin.com/ocr_image/external/45c819e0e2c5b679.jpg)

**Output Image:**

Potholes

Plastic

Other Litter

7

<!-- pothole 0.62 pothole 0.50 pothole 0.89 pothole 0.66 pothole 0.93 pothole 0.87 pothole 0.88 -->
![](https://web-api.textin.com/ocr_image/external/3aad573cb42dfcd1.jpg)

## Positive Image Test 2 - Plastic Bottle

**Test Type**: Positive Image

**Input**: Plastic bottle Image

**Expected**: Plastic should be detected

**Actual**:Plastic detected correctly

**Result:** Pass

Observation:

The system successfully classified the plastic object without confusion.

**Input image:**


![](https://web-api.textin.com/ocr_image/external/4eeba41ce567bba7.jpg)

# Output Image:

<!-- Potholes Plastic Other Litter -->
![](https://web-api.textin.com/ocr_image/external/90b23f197f64fd22.jpg)

# Positive Image Test 3 - Other Litter

**Test Type**:Positive Image

Input: Glass Bottle on the table

**Expected**: Other litter should be detected

**Actual:** Detected as other litter

**Result:** Pass

**Observation:** The model performed well on general waste detection.

**Input image:**


![](https://web-api.textin.com/ocr_image/external/520285a5fec34ba1.jpg)

**Output Image:**

<!-- Potholes Plastic Other Litter 0 0 -->
![](https://web-api.textin.com/ocr_image/external/64a28acd6db191d3.jpg)

# Positive Video Test 1 - Pothole Road

**Test Type**: Positive Video

Input: Video showing road with potholes

**Expected**: Potholes detected in multiple frames

**Actual**: Detected consistently

**Result**: Pass

## Observation:

Stable detection across frames without missing major defects.

# Input video:

Link-&gt; https://drive.google.com/file/d/13KxSa8ahElumlheLmQPDdHeSF7PwmBKw/view?usp=drivelink

# Output video:

Link-&gt; https://drive.google.com/file/d/1vTCHFiG5FjqFq6S2Mv6aznZiV9WrDLei/view?usp=drivelink

# Positive Video Test 2 - Garbage Road

**Test Type**: Positive Video

**Input**: Road with visible garbage

**Expected**: litter detected

**Actual**: classe detected

**Result:** Pass

## Observation:

The system successfully handled other litter in video.

# Input video:

Link-&gt; https://drive.google.com/file/d/14dzd05FvfXyQbjUcloOrz0Y2s2HUmqko/view?usp=drivelink

# Output video:

Link-&gt; https://drive.google.com/file/d/1p25D6rbamL5TpyN77IDkBahFb10JI6z/view?usp=drivelink

# Negative Image Test 1-Clean Road

**Test Type**: Negative Image

Input: Empty clean road

**Expected**: No detection

**Actual:** No bounding boxes

**Result:** Pass

Observation:

The model did not generate false positives.

**Input image:**


![](https://web-api.textin.com/ocr_image/external/c3ee20ea90b64efe.jpg)

**Output image:**

<!-- Potholes Plastic Other Litter 0 0 -->
![](https://web-api.textin.com/ocr_image/external/7ff872c178a3f639.jpg)

## Negative Image Test 2 - Classroom

**Test Type**: Negative Image

**Input**: Indoor classroom image

**Expected**: No detection

**Actual**: No detection

**Result:**Pass

**Observation**: System correctly ignored irrelevant objects.

**Input Image :**


![](https://web-api.textin.com/ocr_image/external/7fb3d414d188738e.jpg)

**Output Image:**

<!-- Potholes Plastic Other Litter 0 -->
![](https://web-api.textin.com/ocr_image/external/f8e91df823ab1e62.jpg)

### Edge Image Test 1 - Blurry Image

**Test Type**: Edge / Partial Correct

Input: Blurry image

**Expected**: May detect or miss

**Actual**: Partial detection

**Result**: Partial Correct

**Observation:**

Blur reduced detection accuracy.

**Input Image:**


![](https://web-api.textin.com/ocr_image/external/eccce8457c1670df.jpg)

## Output Image:

Potholes

Plastic

Other Litter

<!-- 0 -->
![](https://web-api.textin.com/ocr_image/external/5dabf603dfe87e1c.jpg)

## Edge Image Test 2 - Small images

**Test Type**:Edge/Partial Correct

**Input**: Side Road

**Expected**: May detect or miss

**Actual**: Partial detection

**Result**: Partial Correct

**Observation:** Blur reduced detection accuracy.

**Input Image:**


![](https://web-api.textin.com/ocr_image/external/aa0934ab477e5922.jpg)

## Output Image:

<!-- Potholes Plastic Other Litter -->
![](https://web-api.textin.com/ocr_image/external/538cc750d73e15db.jpg)

