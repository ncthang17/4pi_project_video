# pose_keypoint_labelling.py

import sys
import os
import json
import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
from tqdm import tqdm
import subprocess

# -------------------------------
# Step 1: Setup Environment
# -------------------------------

print("🐍 Python executable:", sys.executable)

# Ensure pip is up to date and install required packages
subprocess.run([sys.executable, "-m", "pip", "--version"])
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.run([sys.executable, "-m", "pip", "install", "mediapipe", "opencv-python", "matplotlib", "tqdm"])

# -------------------------------
# Step 2: Static Image Processing Examples
# -------------------------------

def process_single_image(image_path, output_overlay_path, json_output_path, trainee="01", id_="01", frame="001"):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1)
    mp_drawing = mp.solutions.drawing_utils

    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Cannot load image at {image_path}. Check the path.")
        return

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(img_rgb)

    if result.pose_landmarks:
        annotated_img = img.copy()
        mp_drawing.draw_landmarks(annotated_img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        plt.figure(figsize=(8, 8))
        plt.imshow(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB))
        plt.title("Pose Keypoints Check")
        plt.axis('off')
        plt.show()

        cv2.imwrite(output_overlay_path, annotated_img)
        print(f"✅ Overlay saved to {output_overlay_path}")

        keypoint_names = [
            "nose", "left_eye_inner", "left_eye", "left_eye_outer",
            "right_eye_inner", "right_eye", "right_eye_outer",
            "left_ear", "right_ear", "left_shoulder", "right_shoulder",
            "left_elbow", "right_elbow", "left_wrist", "right_wrist"
        ]

        extracted_keypoints = {}
        for idx, name in enumerate(keypoint_names):
            lm = result.pose_landmarks.landmark[idx]
            extracted_keypoints[name] = {
                "x": int(lm.x * img.shape[1]),
                "y": int(lm.y * img.shape[0])
            }

        print("\n✅ Extracted 15 Upper Body Keypoints:")
        for k, v in extracted_keypoints.items():
            print(f"{k}: x={v['x']}, y={v['y']}")

        label_json = {
            "trainee": trainee,
            "id": id_,
            "frame": frame,
            "key_points": extracted_keypoints,
            "emotion": ""
        }
        with open(json_output_path, "w", encoding="utf-8") as f:
            json.dump(label_json, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Saved keypoints to {json_output_path}")
    else:
        print("❌ No keypoints detected. Check image quality and visibility of the upper body in the frame.")

# Examples
process_single_image("01_01_processed_001.png", "checked_overlay.png", "01_01_interview_labelling.json")
process_single_image("01_05_processed_003.png", "checked_overlay_003.png", "01_05_interview_labelling.json")
process_single_image("6_10_processed_007.png", "checked_overlay_007.png", "06_10_interview_labelling.json")

# -------------------------------
# Step 3: Batch Processing Folder
# -------------------------------

def batch_process_images(input_folder="processed_frames", output_json_folder="labelled_json"):
    os.makedirs(output_json_folder, exist_ok=True)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1)

    image_files = [f for f in os.listdir(input_folder) if f.endswith(".png")]

    for file in tqdm(image_files, desc="Processing frames"):
        file_path = os.path.join(input_folder, file)
        try:
            trainee, id_, _, frame_ext = file.split("_")
            frame = frame_ext.split(".")[0]
        except:
            print(f"⚠️ Skipped file due to unexpected name format: {file}")
            continue

        img = cv2.imread(file_path)
        if img is None:
            print(f"❌ Cannot load {file}")
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)

        if result.pose_landmarks:
            h, w, _ = img.shape
            keypoint_names = [
                "nose", "left_eye_inner", "left_eye", "left_eye_outer",
                "right_eye_inner", "right_eye", "right_eye_outer",
                "left_ear", "right_ear", "left_shoulder", "right_shoulder",
                "left_elbow", "right_elbow", "left_wrist", "right_wrist"
            ]

            extracted_keypoints = {}
            for idx, name in enumerate(keypoint_names):
                lm = result.pose_landmarks.landmark[idx]
                extracted_keypoints[name] = {"x": int(lm.x * w), "y": int(lm.y * h)}

            json_data = {
                "trainee": trainee,
                "id": id_,
                "frame": frame,
                "key_points": extracted_keypoints,
                "emotion": ""
            }
            json_name = f"{trainee}_{id_}_frame_{frame}.json"
            with open(os.path.join(output_json_folder, json_name), "w", encoding="utf-8") as jf:
                json.dump(json_data, jf, indent=4, ensure_ascii=False)

        else:
            print(f"⚠️ No keypoints detected in {file}. Check image quality.")

    print("✅ Batch keypoint extraction completed for all frames. JSON files saved in 'labelled_json'.")

batch_process_images()

# -------------------------------
# Step 4: Merge All JSON Files
# -------------------------------

def merge_all_json(json_folder="labelled_json", output_json_file="all_keypoints_labelled.json"):
    json_files = sorted([f for f in os.listdir(json_folder) if f.endswith(".json")])
    all_data = []

    for file in json_files:
        file_path = os.path.join(json_folder, file)
        with open(file_path, "r", encoding="utf-8") as jf:
            data = json.load(jf)
            if isinstance(data, list):
                all_data.extend(data)
            else:
                all_data.append(data)

    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Combined {len(json_files)} JSON files into '{output_json_file}'.")

merge_all_json()

