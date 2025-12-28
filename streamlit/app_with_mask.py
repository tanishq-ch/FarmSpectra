import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)


import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.inference.rust_detector import WheatRustDetector

# --------------------------------
# Load Model via Detector Class
# --------------------------------
MODEL_PATH = "models/trained/best.pt"
detector = WheatRustDetector(MODEL_PATH)

st.set_page_config(page_title="Wheat Rust Evaluation", layout="wide")
st.title("🌾 Wheat Rust Evaluation (Image + Mask)")
st.markdown("Upload a wheat crop image **along with its segmentation mask** for evaluation.")

# --------------------------------
# Upload Inputs
# --------------------------------
uploaded_image = st.file_uploader(
    "Upload Wheat Crop Image",
    type=["jpg", "png", "jpeg"]
)

uploaded_mask = st.file_uploader(
    "Upload Segmentation Mask (PNG)",
    type=["png"]
)

# --------------------------------
# Process Inputs
# --------------------------------
if uploaded_image is not None and uploaded_mask is not None:

    # Load image
    img_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Load mask
    mask_bytes = np.asarray(bytearray(uploaded_mask.read()), dtype=np.uint8)
    gt_mask = cv2.imdecode(mask_bytes, cv2.IMREAD_GRAYSCALE)
    _, gt_mask_bin = cv2.threshold(gt_mask, 127, 255, cv2.THRESH_BINARY)

    # --------------------------------
    # AI Inference
    # --------------------------------
    ai_view, heatmap, boxes = detector.detect(image_rgb)

    # --------------------------------
    # Visualization (2x2 Layout)
    # --------------------------------
    fig, ax = plt.subplots(2, 2, figsize=(16, 16))

    # Panel 1: Original Image
    ax[0, 0].imshow(image_rgb)
    ax[0, 0].set_title("1. Original Image", fontsize=14, fontweight="bold")

    # Panel 2: Ground Truth Mask
    ax[0, 1].imshow(gt_mask_bin, cmap="gray")
    ax[0, 1].set_title("2. Ground Truth Mask", fontsize=14, fontweight="bold")

    # Panel 3: AI Detection
    ax[1, 0].imshow(ai_view)
    for box in boxes:
        x1, y1, x2, y2 = box
        rect = patches.Rectangle(
            (x1, y1),
            x2 - x1,
            y2 - y1,
            linewidth=2,
            edgecolor="yellow",
            facecolor="none"
        )
        ax[1, 0].add_patch(rect)

    ax[1, 0].set_title(
        f"3. AI Detection ({len(boxes)} spots)",
        fontsize=14,
        fontweight="bold"
    )

    # Panel 4: ExG Heatmap
    ax[1, 1].imshow(heatmap)
    ax[1, 1].set_title(
        "4. ExG Vegetation Index Heatmap",
        fontsize=14,
        fontweight="bold"
    )

    for a in ax.flat:
        a.axis("off")

    plt.tight_layout()
    st.pyplot(fig)

    st.success("✅ Evaluation completed successfully")

elif uploaded_image or uploaded_mask:
    st.warning("⚠️ Please upload BOTH the image and its segmentation mask.")
