import streamlit as st
import cv2
import numpy as np

# from utils.ndvi import calculate_ndvi, ndvi_stress_map
# from utils.normalize import normalize, confidence_percentage
# from utils.report import generate_farmer_report
# from utils.voice import generate_hindi_voice

# from main_farmspectra_code import classify_stress
# from drought import drought_score
# from nutrient import nutrient_score

from farmspectra_core import *



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FarmSpectra – Crop Stress Detection",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
body {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
}

/* ===== MAIN CONTAINER ===== */
.main {
    padding: 1.5rem;
}

/* ===== BASE CARD ===== */
.card {
    background: #ffffff;
    padding: 1.4rem;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-bottom: 1.4rem;
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
}

.card-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

/* ===== METRIC COLORS ===== */
.metric-green {
    border-left: 8px solid #4CAF50;
    background: linear-gradient(90deg, #e8f5e9, #ffffff);
}

.metric-yellow {
    border-left: 8px solid #FFC107;
    background: linear-gradient(90deg, #fff8e1, #ffffff);
}

.metric-red {
    border-left: 8px solid #F44336;
    background: linear-gradient(90deg, #ffebee, #ffffff);
}

.metric-brown {
    border-left: 8px solid #795548;
    background: linear-gradient(90deg, #efebe9, #ffffff);
}

/* ===== INFO CARDS ===== */
.info-blue {
    border-left: 8px solid #2196F3;
    background: #e3f2fd;
}

.info-orange {
    border-left: 8px solid #FF9800;
    background: #fff3e0;
}

.center {
    text-align: center;
}

/* ===== BUTTONS ===== */
.stButton > button {
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<div class="card center">
    <h1>🌱 FarmSpectra</h1>
    <p>Smart Crop Stress Detection & Advisory System</p>
</div>
""", unsafe_allow_html=True)


# ---------------- FILE UPLOAD ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📷 Upload RGB Image</div>', unsafe_allow_html=True)
    rgb_file = st.file_uploader("", ["png", "jpg", "jpeg"], key="rgb")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📡 Upload NIR Image</div>', unsafe_allow_html=True)
    nir_file = st.file_uploader("", ["png", "jpg", "jpeg"], key="nir")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- PROCESSING ----------------
if rgb_file and nir_file:
    rgb = cv2.imdecode(np.frombuffer(rgb_file.read(), np.uint8), cv2.IMREAD_COLOR)
    nir = cv2.imdecode(np.frombuffer(nir_file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

    ndvi = calculate_ndvi(rgb, nir)
    ndvi_mean = float(ndvi.mean())
    status = classify_stress(ndvi_mean)

    # ---------------- SUMMARY ----------------
    s1, s2 = st.columns(2)

    with s1:
        st.markdown('<div class="card info-blue">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🌾 Field Health</div>', unsafe_allow_html=True)
        st.write("❌ Field is under stress" if status == "Stressed" else "✅ Field is healthy")
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📈 NDVI Insight</div>', unsafe_allow_html=True)
        st.metric("Mean NDVI", round(ndvi_mean, 3))
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- MAP ----------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗺️ Field Stress Map</div>', unsafe_allow_html=True)
    fig, stress_map = ndvi_stress_map(ndvi)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- METRICS ----------------
    total = stress_map.size
    barren = (stress_map == 0).sum() / total * 100
    severe = (stress_map == 1).sum() / total * 100
    moderate = (stress_map == 2).sum() / total * 100
    healthy = (stress_map == 3).sum() / total * 100

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown('<div class="card metric-green center">', unsafe_allow_html=True)
        st.metric("🌾 Healthy", f"{healthy:.0f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with m2:
        st.markdown('<div class="card metric-yellow center">', unsafe_allow_html=True)
        st.metric("⚠️ Moderate", f"{moderate:.0f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with m3:
        st.markdown('<div class="card metric-red center">', unsafe_allow_html=True)
        st.metric("❌ Severe", f"{severe:.0f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    with m4:
        st.markdown('<div class="card metric-brown center">', unsafe_allow_html=True)
        st.metric("🟤 Barren", f"{barren:.0f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- DIAGNOSIS ----------------
    d_val = normalize(drought_score(ndvi))
    n_val = normalize(nutrient_score(ndvi))

    d1, d2 = st.columns(2)

    with d1:
        st.markdown('<div class="card info-blue">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔍 Cause of Stress</div>', unsafe_allow_html=True)
        main_issue = "Drought Stress" if d_val > n_val else "Nutrient Deficiency"
        st.write(main_issue)
        st.markdown('</div>', unsafe_allow_html=True)

    with d2:
        st.markdown('<div class="card info-orange">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🤝 Confidence</div>', unsafe_allow_html=True)
        conf = confidence_percentage(d_val, n_val)
        st.progress(conf / 100)
        st.write(f"{conf}% confidence")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- ACTIONS ----------------
    a1, a2 = st.columns(2)

    with a1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🧑‍🌾 Recommended Action</div>', unsafe_allow_html=True)
        st.write("Improve irrigation & watering frequency" if "Drought" in main_issue else "Apply recommended fertilizers")
        st.markdown('</div>', unsafe_allow_html=True)

    with a2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📄 Report & 🔊 Audio</div>', unsafe_allow_html=True)

        if st.button("📄 Download PDF"):
            generate_farmer_report("FarmSpectra_Report.pdf", status, main_issue, healthy, moderate, severe, barren)
            with open("FarmSpectra_Report.pdf", "rb") as f:
                st.download_button("⬇️ Download", f)

        if st.button("▶️ Hindi Audio Summary"):
            generate_hindi_voice("farm_voice_hindi.mp3", status, main_issue, healthy, moderate, severe, barren)
            st.audio(open("farm_voice_hindi.mp3", "rb").read(), format="audio/mp3")

        st.markdown('</div>', unsafe_allow_html=True)
