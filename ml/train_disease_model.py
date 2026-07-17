"""
train_disease_model.py — Step 2 of Module 3 (Crop Disease Detection)

Trains an image classifier on the 10 Tomato disease/healthy classes
from the PlantVillage dataset, using transfer learning (MobileNetV2).

Run this from inside the ml/ folder with the ML venv (Python 3.11) active:
    python train_disease_model.py

This will take roughly 20-40+ minutes on a laptop CPU, depending on
your hardware. Do not close the terminal while it's training.

Output: a file called tomato_disease_model.h5 saved in this folder.
"""

import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ---- CONFIG ----
DATASET_PATH = r"C:\Users\divya\.cache\kagglehub\datasets\emmarex\plantdisease\versions\1\PlantVillage"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 8  # keep this modest for a laptop CPU; can increase later if time allows

# Only these folders will be used for training (Tomato classes only)
TOMATO_CLASSES = [
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_healthy",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_mosaic_virus",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
]


def build_filtered_dataset_dir():
    """
    ImageDataGenerator needs a directory containing ONLY the classes we want.
    Since the PlantVillage folder has Pepper/Potato/Tomato mixed together,
    we create a temporary folder with symlinks/copies of just the Tomato subfolders.
    """
    filtered_dir = os.path.join(os.getcwd(), "tomato_dataset")
    os.makedirs(filtered_dir, exist_ok=True)

    for class_name in TOMATO_CLASSES:
        source = os.path.join(DATASET_PATH, class_name)
        dest = os.path.join(filtered_dir, class_name)

        if not os.path.exists(source):
            print(f"WARNING: {source} not found, skipping.")
            continue

        if not os.path.exists(dest):
            # Use a junction/symlink if possible, otherwise copy (Windows-safe fallback)
            try:
                os.symlink(source, dest, target_is_directory=True)
            except (OSError, NotImplementedError):
                import shutil
                print(f"  Copying {class_name} (symlink not available)...")
                shutil.copytree(source, dest)

    return filtered_dir


def train_model():
    print("Preparing dataset (filtering to Tomato classes only)...")
    filtered_dir = build_filtered_dataset_dir()

    print("\nSetting up data generators (80% train / 20% validation split)...")
    datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.2,
        rotation_range=20,
        horizontal_flip=True,
    )

    train_data = datagen.flow_from_directory(
        filtered_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training",
    )

    val_data = datagen.flow_from_directory(
        filtered_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
    )

    num_classes = train_data.num_classes
    print(f"\nFound {num_classes} classes: {list(train_data.class_indices.keys())}")

    # Save class names in the correct order for later use during prediction
    class_names = list(train_data.class_indices.keys())
    with open("class_names.txt", "w") as f:
        f.write("\n".join(class_names))

    print("\nBuilding model (MobileNetV2 transfer learning)...")
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # freeze pretrained layers

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    print(f"\nStarting training for {EPOCHS} epochs... this will take a while.\n")
    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=EPOCHS,
    )

    model.save("tomato_disease_model.h5")
    print("\nDONE. Model saved as tomato_disease_model.h5")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.2%}")


if __name__ == "__main__":
    train_model()