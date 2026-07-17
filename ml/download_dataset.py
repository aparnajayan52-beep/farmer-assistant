"""
download_dataset.py — Step 1 of Module 3 (Crop Disease Detection)

Downloads the PlantVillage dataset (leaf images labeled by disease)
using kagglehub. This may take a few minutes depending on your
internet speed, since the dataset is a few hundred MB.

Run this from inside the ml/ folder with the ML venv active:
    python download_dataset.py
"""

import kagglehub

print("Downloading PlantVillage dataset... this may take a few minutes.")

# This downloads the dataset and caches it locally.
# It prints the path where the dataset was saved.
path = kagglehub.dataset_download("emmarex/plantdisease")

print(f"\nDataset downloaded successfully!")
print(f"Path: {path}")
print("\nExplore this folder to see the structure — it should contain")
print("subfolders named after crop + disease combinations (e.g. Tomato___Early_blight),")
print("each full of labeled leaf images.")