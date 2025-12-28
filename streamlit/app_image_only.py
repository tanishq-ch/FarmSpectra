import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)


import streamlit as st
import cv2
import numpy as np
from src.inference.rust_detector import WheatRustDetector

detector = WheatRustDetector("models/trained/best.pt")

st.set_page_config(layout="wide")
st.title("🌾 Wheat Rust Detection – Image Only")

uploaded = st.file_uploader("Upload Wheat Image", type=["jpg","png","jpeg"])

if uploaded:
    img_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    ai_view, heatmap, boxes = detector.detect(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image)
        st.subheader(f"AI Detection ({len(boxes)} spots)")
        st.image(ai_view)

    with col2:
        st.subheader("ExG Heatmap")
        st.image(heatmap)
        
    if len(boxes) == 0:
    	st.warning(
        "⚠️ No rust detected. This may be due to:\n"
        "- Very early-stage disease\n"
        "- Healthy crop image\n"
        "- Different field conditions than training data"
    )


