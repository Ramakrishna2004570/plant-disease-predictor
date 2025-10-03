import cv2
import numpy as np
import os
import shutil

# --- Configuration ---
# The percentage of spots to be considered "Severe". We can tune this value.
SEVERE_THRESHOLD = 0.15  # Let's start with 15%

# --- Paths based on your new project structure ---
RAW_DIR = 'data/raw'
PROCESSED_DIR = 'data/processed'

# --- Class Definitions ---
CLASSES = {
    'Potato___Early_blight': ('Early_Blight_Mild', 'Early_Blight_Severe'),
    'Potato___Late_blight': ('Late_Blight_Mild', 'Late_Blight_Severe'),
    'Potato___healthy': ('Healthy', None)
}

def get_spot_ratio(image_path):
    """Calculates the ratio of dark spots to the total leaf area."""
    try:
        image = cv2.imread(image_path)
        if image is None: return 0.0
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Use a threshold to create a binary mask of dark spots
        _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
        return np.count_nonzero(mask) / (image.shape[0] * image.shape[1])
    except Exception:
        return 0.0

def process_images():
    """Sorts images from raw folders into processed severity folders."""
    print("Starting image sorting...")
    # Create the destination folders
    for mild, severe in CLASSES.values():
        if mild: os.makedirs(os.path.join(PROCESSED_DIR, mild), exist_ok=True)
        if severe: os.makedirs(os.path.join(PROCESSED_DIR, severe), exist_ok=True)

    for raw_folder, (mild, severe) in CLASSES.items():
        source_path = os.path.join(RAW_DIR, raw_folder)
        if not os.path.exists(source_path):
            print(f"Warning: Raw data folder not found at {source_path}")
            continue

        print(f"Processing folder: {raw_folder}...")
        for filename in os.listdir(source_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                src_file = os.path.join(source_path, filename)
                dest_folder = mild
                if severe:  # This check handles the 'Healthy' class
                    ratio = get_spot_ratio(src_file)
                    if ratio >= SEVERE_THRESHOLD:
                        dest_folder = severe

                shutil.copy(src_file, os.path.join(PROCESSED_DIR, dest_folder))

    print("\nImage sorting complete.")
    print("Final image counts:")
    for folder in sorted(os.listdir(PROCESSED_DIR)):
        count = len(os.listdir(os.path.join(PROCESSED_DIR, folder)))
        print(f"- {folder}: {count} images")

if __name__ == '__main__':
    process_images()
