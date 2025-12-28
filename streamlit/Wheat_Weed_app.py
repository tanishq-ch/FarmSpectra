import streamlit as st
import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from ultralytics import YOLO

def run_weed_detection():
# =================================================
# PAGE SETUP
# =================================================
# st.set_page_config(
#     page_title="FarmSpectra: Weed Detection",
#     page_icon="🌾",
#     layout="wide"
# )

# =================================================
# CUSTOM CSS
# =================================================
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa, #e6f2ea);
    }
    .header-box {
        background: linear-gradient(120deg, #2ecc71, #27ae60);
        padding: 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
        margin-bottom: 30px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
    }
    .low { background:#fff3cd; color:#856404; }
    .medium { background:#ffeeba; color:#856404; }
    .high { background:#f8d7da; color:#721c24; }
    .none { background:#d4edda; color:#155724; }

    .stButton>button {
        background: linear-gradient(120deg, #2ecc71, #27ae60);
        color: white;
        border-radius: 30px;
        font-weight: 700;
        padding: 10px 28px;
        font-size: 16px;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # =================================================
    # HEADER
    # =================================================
    st.markdown("""
    <div class="header-box">
        <h1>🌾 FarmSpectra: Weed Detection System</h1>
        <p style="font-size:18px;">
            YOLO Weed Detection with Smart Farmer Guidance
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =================================================
    # DEVICE
    # =================================================
    if torch.cuda.is_available():
        DEVICE = "cuda"
    elif torch.backends.mps.is_available():
        DEVICE = "mps"
    else:
        DEVICE = "cpu"

    st.info(f"⚙️ Running on **{DEVICE.upper()}**")

    # =================================================
    # MODEL PATH
    # =================================================
    WHEAT_MODEL_PATH = "E:/Disease_FinalYear/models/trained/weed_detector_best.pt"

    # =================================================
    # SESSION STATE
    # =================================================
    if "run_detection" not in st.session_state:
        st.session_state.run_detection = False

    # =================================================
    # UPLOAD
    # =================================================
    st.markdown("## 📤 Upload RGB Field Image")
    uploaded_file = st.file_uploader(
        "Supported formats: JPG, PNG, JPEG",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("🔍 Run Weed Detection"):
        st.session_state.run_detection = True

    if uploaded_file is None:
        st.warning("👆 Please upload a wheat field image to begin.")
        st.stop()

    # =================================================
    # LOAD IMAGE
    # =================================================
    image = Image.open(uploaded_file).convert("RGB")
    img_w, img_h = image.size

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'><h3>📷 Original Image</h3></div>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)

    # =================================================
    # LOAD MODEL
    # =================================================
    @st.cache_resource
    def load_wheat_model():
        return YOLO(WHEAT_MODEL_PATH)

    # =================================================
    # HIGH-VISIBILITY DRAW BOXES
    # =================================================
    def draw_boxes(img, boxes, scores):
        overlay = img.copy()
        draw_overlay = ImageDraw.Draw(overlay)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        for i, ((x1, y1, x2, y2), s) in enumerate(zip(boxes, scores), 1):
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            # Semi-transparent red fill
            draw_overlay.rectangle(
                [x1, y1, x2, y2],
                fill=(255, 0, 0, 80)
            )

            # Thick border
            draw.rectangle(
                [x1, y1, x2, y2],
                outline="red",
                width=5
            )

            label = f"Weed {i} | {s:.2f}"

            text_box = draw.textbbox((x1, y1), label, font=font)
            draw.rectangle(
                [text_box[0]-6, text_box[1]-6, text_box[2]+6, text_box[3]+6],
                fill="black"
            )
            draw.text((x1, y1), label, fill="white", font=font)

        return Image.blend(img, overlay, alpha=0.35)

    # =================================================
    # RUN DETECTION
    # =================================================
    if st.session_state.run_detection:

        model = load_wheat_model()

        with st.spinner("🤖 Analyzing your field..."):
            results = model(
                np.array(image),
                conf=0.25,
                iou=0.5,
                device=DEVICE
            )[0]

        final_boxes, final_scores = [], []

        for box in results.boxes:
            final_boxes.append(box.xyxy[0].tolist())
            final_scores.append(float(box.conf[0]))

        weed_count = len(final_boxes)
        avg_conf = sum(final_scores) / len(final_scores) if weed_count else 0.0

        with col2:
            st.markdown("<div class='card'><h3>🧠 Prediction</h3></div>", unsafe_allow_html=True)
            if weed_count > 0:
                st.image(draw_boxes(image.copy(), final_boxes, final_scores), use_container_width=True)
            else:
                st.image(image, caption="No weeds detected", use_container_width=True)

        # =================================================
        # SUMMARY
        # =================================================
        st.markdown("## 📊 Detection Summary")

        if weed_count == 0:
            severity, css = "None", "none"
        elif weed_count <= 3:
            severity, css = "Low", "low"
        elif weed_count <= 7:
            severity, css = "Moderate", "medium"
        else:
            severity, css = "Severe", "high"

        st.markdown(f"""
        <div class="card">
            <h4>🌱 Weeds Detected: <b>{weed_count}</b></h4>
            <p>Average Confidence: <b>{avg_conf:.2f}</b></p>
            <span class="badge {css}">Severity: {severity}</span>
        </div>
        """, unsafe_allow_html=True)

        # =================================================
        # ADVISORY
        # =================================================
        st.markdown("## 🧑‍🌾 Farmer Advisory")

        if severity == "None":
            st.success("✅ Crop is healthy. Continue regular monitoring.")
        elif severity == "Low":
            st.warning("🟡 Manual weeding recommended. Monitor every 3–4 days.")
        elif severity == "Moderate":
            st.warning("🟠 Apply selective herbicide within 48–72 hours.")
        else:
            st.error("🔴 Immediate action required. Contact agricultural officer.")

        # =================================================
        # QUESTIONS
        # =================================================
        st.markdown("## 💬 Ask Questions (Hindi & English)")

        with st.expander("🌾 Common Questions"):
            st.markdown("""
            **Will weeds reduce yield?**  
            ➤ Yes, uncontrolled weeds reduce wheat yield significantly.

            **खरपतवार फसल को नुकसान करेंगे?**  
            ➤ हाँ, समय पर नियंत्रण जरूरी है।

            **When should I act?**  
            ➤ Severe cases: within 24–48 hours.
            """)

        user_q = st.text_input("Ask your question")

        if user_q:
            q = user_q.lower()
            if "time" in q or "समय" in q:
                st.success("⏱️ Improvement seen in 5–7 days after treatment.")
            elif "herbicide" in q or "दवा" in q:
                st.success("💊 Use wheat-specific selective herbicides only.")
            elif "yield" in q or "पैदावार" in q:
                st.success("📉 Yield loss can reach 30–50% if untreated.")
            else:
                st.info("📞 Consult your local agricultural expert.")

        # =================================================
        # DOWNLOAD
        # =================================================
        st.markdown("## 📥 Download Report")
        st.download_button(
            "📄 Download Report",
            data=f"""
    Crop: Wheat
    Weeds Detected: {weed_count}
    Average Confidence: {avg_conf:.2f}
    Severity: {severity}
    """,
            file_name="wheat_weed_detection_report.txt"
        )
if __name__ == "__main__":
    run_weed_detection()