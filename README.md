
# 🧍‍♂️ Pose Keypoint Labelling Tool

This project provides a pipeline for labelling **15 upper body keypoints** from static pose images using [MediaPipe Pose](https://developers.google.com/mediapipe/solutions/vision/pose). It includes tools for:

- Processing and labelling single or batch images
- Visualizing pose landmarks
- Exporting keypoints into JSON files
- Merging labelled results
- Standardizing filenames for image input

---

## 📂 Project Structure

```
4pi_project_video/
├── keypoint.py             # Main script for pose estimation and keypoint labelling
├── rename.py               # Optional utility for renaming image files to a consistent format
├── processed_frames/       # Input image folder (e.g., .png frames)
├── labelled_json/          # Output folder for labelled JSON files
├── all_keypoints_labelled.json  # Merged JSON output
├── example_image.png       # Example input image
└── README.md               # Project documentation
```

---

## 🛠 Requirements

Python ≥ 3.7  
Install dependencies:

```bash
pip install --upgrade pip
pip install mediapipe opencv-python matplotlib tqdm
```

Alternatively, these are installed automatically when you run `keypoint.py`.

---

## 🚀 Usage

### 1️⃣ Label a Single Image

```bash
python keypoint.py
```

This will:
- Load a `.png` image
- Detect 15 upper body keypoints using MediaPipe
- Visualize and overlay keypoints
- Save results to `.json` format

The function used:

```python
process_single_image(image_path, overlay_output_path, json_output_path, trainee="01", id_="01", frame="001")
```

---

### 2️⃣ Batch Process All Images

Processes every `.png` file in the `processed_frames/` folder and saves keypoints as JSON files to `labelled_json/`.

```python
batch_process_images(input_folder="processed_frames", output_json_folder="labelled_json")
```

---

### 3️⃣ Merge All JSON Files

Combine all JSON files in `labelled_json/` into one master file:

```python
merge_all_json(json_folder="labelled_json", output_json_file="all_keypoints_labelled.json")
```

---

### 4️⃣ Standardize Filenames (Optional)

To ensure filenames follow the format `XX_XX_processed_XXX.png` (e.g., `01_05_processed_007.png`):

```bash
python rename.py
```

This will:
- Rename images in `processed_frames/`
- Match any loosely formatted files (e.g., `1-5_frame7.png`) to the strict format

---

## 📌 Keypoint Format

Each JSON contains:

```json
{
  "trainee": "01",
  "id": "05",
  "frame": "003",
  "key_points": {
    "nose": {"x": 123, "y": 456},
    "left_eye_inner": {"x": 124, "y": 457},
    ...
  },
  "emotion": ""
}
```
