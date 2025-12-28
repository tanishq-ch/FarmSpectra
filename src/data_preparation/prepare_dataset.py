# ==========================================
# STEP 1: PREPARE NWRD DATASET (High Sensitivity)
# ==========================================
import os
import shutil
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

# --- CONFIG ---
ZIP_FILENAME = "/content/drive/MyDrive/NWRD.zip"  # Check this path matches yours!
EXTRACT_DIR = "NWRD_Raw"
YOLO_DIR = "NWRD_YOLO"

# 1. Unzip
if os.path.exists(EXTRACT_DIR): shutil.rmtree(EXTRACT_DIR)
try:
    shutil.unpack_archive(ZIP_FILENAME, EXTRACT_DIR)
    print("✅ Unzip Successful.")
except Exception as e:
    print(f"❌ Error unzipping: {e}")
    raise e

# 2. Setup YOLO Directory
if os.path.exists(YOLO_DIR): shutil.rmtree(YOLO_DIR)
for folder in ['train', 'val']:
    os.makedirs(os.path.join(YOLO_DIR, folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(YOLO_DIR, folder, 'labels'), exist_ok=True)

# 3. Improved Conversion Function (Captures Small Spots)
def convert_mask_to_yolo(mask_path, label_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None: return False

    # Threshold
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    H, W = mask.shape
    yolo_lines = []

    for cnt in contours:
        # --- FIX 1: Lower threshold to keep tiny rust spots ---
        if cv2.contourArea(cnt) < 10: continue

        # --- FIX 2: Less smoothing for accurate shapes ---
        cnt = cv2.approxPolyDP(cnt, 0.002 * cv2.arcLength(cnt, True), True)

        points = []
        for point in cnt:
            x, y = point[0]
            points.append(f"{x/W:.6f} {y/H:.6f}")

        if len(points) > 2:
            yolo_lines.append(f"0 {' '.join(points)}")

    if yolo_lines:
        with open(label_path, 'w') as f:
            f.write('\n'.join(yolo_lines))
        return True
    return False

# 4. Process Structure
print("🔄 Processing NWRD Structure...")
base_search_path = os.path.join(EXTRACT_DIR, "NWRD")
if not os.path.exists(base_search_path):
    for root, dirs, files in os.walk(EXTRACT_DIR):
        if 'train' in dirs:
            base_search_path = root
            break

def process_subset(subset_name, is_train_val=True):
    img_dir = os.path.join(base_search_path, subset_name, 'images')
    mask_dir = os.path.join(base_search_path, subset_name, 'masks')

    if not os.path.exists(img_dir): return

    images = [f for f in os.listdir(img_dir) if f.lower().endswith('.jpg')]

    for filename in images:
        name_no_ext = os.path.splitext(filename)[0]
        mask_path = os.path.join(mask_dir, name_no_ext + ".png")
        img_src = os.path.join(img_dir, filename)

        if is_train_val:
            dest_split = 'train' if np.random.rand() > 0.1 else 'val'
        else:
            dest_split = 'val'

        img_dst = os.path.join(YOLO_DIR, dest_split, 'images', filename)
        label_dst = os.path.join(YOLO_DIR, dest_split, 'labels', name_no_ext + ".txt")

        if os.path.exists(mask_path):
            if convert_mask_to_yolo(mask_path, label_dst):
                shutil.copy(img_src, img_dst)

process_subset('train', is_train_val=True)
process_subset('test', is_train_val=False)

# 5. Create YAML
yaml_content = f"""
path: {os.path.abspath(YOLO_DIR)}
train: train/images
val: val/images
names:
  0: Wheat_Rust
"""
with open(f"{YOLO_DIR}/data.yaml", 'w') as f:
    f.write(yaml_content)

print("✅ Dataset Ready (High Sensitivity Mode)!")