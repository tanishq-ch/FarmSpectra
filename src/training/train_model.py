# ==========================================
# STEP 2: TRAIN YOLO SEGMENTATION (High Accuracy)
# ==========================================

import ultralytics
from ultralytics import YOLO

# --- FIX 3: Use Medium model (Smarter than Nano) ---
model = YOLO('yolov8m-seg.pt')

print("🚀 Starting Training (High Res Mode)...")
results = model.train(
    data=f"{YOLO_DIR}/data.yaml",
    epochs=50,
    imgsz=1024,         # --- FIX 4: Higher resolution to see small spots ---
    batch=8,            # Lower batch size for memory safety
    name='nwrd_rust_detector',
    project='wheat_project'
)
print("✅ Training Complete.")