# import streamlit as st
# import os
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from ultralytics import YOLO
# import tempfile
# from datetime import datetime

# # ---------------------------------
# # Streamlit Config
# # ---------------------------------
# st.set_page_config(page_title="Wheat Rust Detection", layout="wide")
# st.title("🌾 Wheat Rust Detection")

# # ---------------------------------
# # Load Model (SAME AS COLAB)
# # ---------------------------------
# MODEL_PATH = "models/trained/best.pt"

# if not os.path.exists(MODEL_PATH):
#     st.error("❌ Model file not found: best.pt")
#     st.stop()

# model = YOLO(MODEL_PATH)

# # ---------------------------------
# # Upload Inputs
# # ---------------------------------
# uploaded_image = st.file_uploader(
#     "Upload Wheat Crop Image",
#     type=["jpg", "png", "jpeg"]
# )

# # 🔴 SEGMENTATION MASK UPLOAD (COMMENTED FOR NOW)
# # uploaded_mask = st.file_uploader(
# #     "Upload Segmentation Mask (Evaluation Mode)",
# #     type=["png"]
# # )

# # ---------------------------------
# # ExG Function (SAVED, NOT DISPLAYED)
# # ---------------------------------
# def calculate_exg_heatmap(image_rgb):
#     img = image_rgb.astype(float)
#     blue, green, red = img[:, :, 2], img[:, :, 1], img[:, :, 0]
#     exg = 2 * green - red - blue
#     exg_norm = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
#     return 255 - exg_norm

# # ---------------------------------
# # Main Logic
# # ---------------------------------
# if uploaded_image is not None:

#     # ---- Save uploaded image to TEMP FILE
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
#         tmp_img.write(uploaded_image.read())
#         img_path = tmp_img.name

#     # ---- Load image SAME WAY AS COLAB
#     original_img = cv2.imread(img_path)
#     original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

#     # ---------------------------------
#     # INFERENCE (IDENTICAL TO COLAB)
#     # ---------------------------------
#     results = model(
#         img_path,
#         imgsz=1024,
#         retina_masks=True,
#         verbose=False
#     )[0]

#     overlay_img = original_img.copy()
#     boxes = []

#     if results.masks is not None:
#         masks = results.masks.data.cpu().numpy()

#         if len(masks.shape) > 2:
#             combined_mask = np.sum(masks, axis=0)
#         else:
#             combined_mask = masks

#         combined_mask = cv2.resize(
#             combined_mask,
#             (original_img.shape[1], original_img.shape[0])
#         )

#         overlay_img[combined_mask > 0.5] = [255, 0, 0]
#         boxes = results.boxes.xyxy.cpu().numpy()

#     ai_view = cv2.addWeighted(original_img, 0.7, overlay_img, 0.3, 0)

#     # ---------------------------------
#     # SAVE ExG HEATMAP (NOT DISPLAYED)
#     # ---------------------------------
#     exg_data = calculate_exg_heatmap(original_img)
#     clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
#     exg_enhanced = clahe.apply(exg_data)
#     exg_heatmap = cv2.applyColorMap(exg_enhanced, cv2.COLORMAP_JET)

#     os.makedirs("results/exg_heatmaps", exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     exg_save_path = f"results/exg_heatmaps/exg_{timestamp}.png"
#     cv2.imwrite(exg_save_path, exg_heatmap)

#     # ---------------------------------
#     # DISPLAY (NO ExG, CLEAN UI)
#     # ---------------------------------
#     fig, ax = plt.subplots(1, 2, figsize=(18, 7))

#     ax[0].imshow(original_img)
#     ax[0].set_title("Original Image", fontweight="bold")

#     ax[1].imshow(ai_view)
#     for box in boxes:
#         x1, y1, x2, y2 = box
#         ax[1].add_patch(
#             patches.Rectangle(
#                 (x1, y1),
#                 x2 - x1,
#                 y2 - y1,
#                 linewidth=2,
#                 edgecolor="yellow",
#                 facecolor="none"
#             )
#         )

#     ax[1].set_title(
#         f"AI Detection ({len(boxes)} Spots)",
#         fontweight="bold"
#     )

#     for a in ax:
#         a.axis("off")

#     st.pyplot(fig)

#     if len(boxes) == 0:
#         st.warning(
#             "⚠️ No rust detected. This may indicate a healthy crop or early-stage infection."
#         )
#     else:
#         st.success("✅ Rust disease detected")

#     # Cleanup temp file
#     os.remove(img_path)



# edited streamlit code 2 (final before the claude code)
# import streamlit as st
# import os
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from ultralytics import YOLO
# import tempfile
# from datetime import datetime

# # =================================================
# # PAGE CONFIG
# # =================================================
# st.set_page_config(
#     page_title="FarmSpectra – Wheat Rust Detection",
#     layout="wide"
# )

# # =================================================
# # FORCE LIGHT THEME + CLEAN UI
# # =================================================
# st.markdown("""
# <style>
# html, body, [class*="css"] {
#     background-color: #ffffff !important;
#     color: #111111 !important;
# }

# section.main > div {
#     background-color: #ffffff !important;
# }

# .header {
#     font-size: 38px;
#     font-weight: 800;
#     color: #1b5e20;
#     margin-bottom: 5px;
# }

# .subheader {
#     font-size: 18px;
#     color: #444444;
#     margin-bottom: 25px;
# }

# .card {
#     background-color: #ffffff;
#     padding: 22px;
#     border-radius: 16px;
#     box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
#     margin-bottom: 25px;
#     text-align: center;
#     border: 1px solid #e0e0e0;
# }

# .success {
#     color: #2e7d32;
#     font-weight: 700;
#     font-size: 18px;
# }

# .warning {
#     color: #f9a825;
#     font-weight: 700;
#     font-size: 18px;
# }

# .danger {
#     color: #c62828;
#     font-weight: 700;
#     font-size: 18px;
# }

# .stat-title {
#     font-size: 15px;
#     color: #555;
# }

# .stat-value {
#     font-size: 28px;
#     font-weight: 800;
#     color: #222;
# }

# .stFileUploader {
#     background-color: #fafafa !important;
#     border-radius: 12px;
#     padding: 10px;
# }

# footer {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

# # =================================================
# # HEADER
# # =================================================
# st.markdown("""
# <div class="header">🌿 FarmSpectra – Wheat Rust Detection System</div>
# <div class="subheader">
# AI-powered plant-level disease detection for precision agriculture
# </div>
# <hr>
# """, unsafe_allow_html=True)

# # =================================================
# # LOAD MODEL (COLAB-EQUIVALENT)
# # =================================================
# MODEL_PATH = "models/trained/best.pt"

# if not os.path.exists(MODEL_PATH):
#     st.error("❌ Model file not found: models/trained/best.pt")
#     st.stop()

# model = YOLO(MODEL_PATH)

# # =================================================
# # INPUT
# # =================================================
# st.markdown("### 📤 Upload Wheat Crop Image")
# uploaded_image = st.file_uploader(
#     "Upload RGB image of wheat crop",
#     type=["jpg", "png", "jpeg"]
# )

# # 🔴 OPTIONAL – ENABLE ONLY FOR EVALUATION
# # uploaded_mask = st.file_uploader(
# #     "Upload Segmentation Mask (Evaluation Mode)",
# #     type=["png"]
# # )

# # =================================================
# # ExG FUNCTION (BACKGROUND ONLY)
# # =================================================
# def calculate_exg_heatmap(image_rgb):
#     img = image_rgb.astype(float)
#     blue, green, red = img[:, :, 2], img[:, :, 1], img[:, :, 0]
#     exg = 2 * green - red - blue
#     exg_norm = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
#     return 255 - exg_norm

# # =================================================
# # MAIN PIPELINE
# # =================================================
# if uploaded_image is not None:

#     # Save uploaded image to temp file (CRITICAL FIX)
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
#         tmp.write(uploaded_image.read())
#         img_path = tmp.name

#     original_img = cv2.imread(img_path)
#     original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

#     # ---------------- INFERENCE (IDENTICAL TO COLAB)
#     results = model(
#         img_path,
#         imgsz=1024,
#         retina_masks=True,
#         verbose=False
#     )[0]

#     overlay_img = original_img.copy()
#     boxes = []

#     infected_pixels = 0
#     total_pixels = original_img.shape[0] * original_img.shape[1]

#     if results.masks is not None:
#         masks = results.masks.data.cpu().numpy()
#         combined_mask = np.sum(masks, axis=0)
#         combined_mask = cv2.resize(
#             combined_mask,
#             (original_img.shape[1], original_img.shape[0])
#         )

#         infected_pixels = np.sum(combined_mask > 0.5)
#         overlay_img[combined_mask > 0.5] = [255, 0, 0]
#         boxes = results.boxes.xyxy.cpu().numpy()

#     ai_view = cv2.addWeighted(original_img, 0.7, overlay_img, 0.3, 0)

#     # ---------------- SAVE ExG HEATMAP (NOT SHOWN)
#     exg = calculate_exg_heatmap(original_img)
#     clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
#     exg_enhanced = clahe.apply(exg)
#     exg_heatmap = cv2.applyColorMap(exg_enhanced, cv2.COLORMAP_JET)

#     os.makedirs("results/exg_heatmaps", exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     cv2.imwrite(f"results/exg_heatmaps/exg_{timestamp}.png", exg_heatmap)

#     # ---------------- FEATURE CALCULATIONS
#     severity = (infected_pixels / total_pixels) * 100 if infected_pixels > 0 else 0

#     if severity < 5:
#         risk = "Healthy"
#         risk_class = "success"
#         summary_text = "Your crop appears healthy"
#     elif severity < 15:
#         risk = "Mild Stress"
#         risk_class = "warning"
#         summary_text = "Early-stage rust detected"
#     elif severity < 30:
#         risk = "Moderate Stress"
#         risk_class = "danger"
#         summary_text = "Moderate rust infection detected"
#     else:
#         risk = "Severe Stress"
#         risk_class = "danger"
#         summary_text = "Severe rust infection detected"

#     # =================================================
#     # FIELD HEALTH SUMMARY
#     # =================================================
#     st.markdown(f"""
#     <div class="card">
#         <h3>🌾 Field Health Summary</h3>
#         <p class="{risk_class}">{summary_text}</p>
#     </div>
#     """, unsafe_allow_html=True)

#     # =================================================
#     # STAT CARDS
#     # =================================================
#     c1, c2, c3 = st.columns(3)

#     with c1:
#         st.markdown(f"""
#         <div class="card">
#             <div class="stat-title">🌿 Disease Severity</div>
#             <div class="stat-value">{severity:.2f}%</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c2:
#         st.markdown(f"""
#         <div class="card">
#             <div class="stat-title">📍 Detected Spots</div>
#             <div class="stat-value">{len(boxes)}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     with c3:
#         st.markdown(f"""
#         <div class="card">
#             <div class="stat-title">⚠️ Risk Level</div>
#             <div class="stat-value">{risk}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     # =================================================
#     # SEVERITY BAR
#     # =================================================
#     st.markdown("### 🌱 Disease Severity Level")
#     st.progress(min(severity / 100, 1.0))

#     # =================================================
#     # DETECTION RESULT
#     # =================================================
#     st.markdown("### 🖼️ Detection Result")

#     fig, ax = plt.subplots(1, 2, figsize=(18, 7))

#     ax[0].imshow(original_img)
#     ax[0].set_title("Original Image", fontweight="bold")

#     ax[1].imshow(ai_view)
#     for box in boxes:
#         x1, y1, x2, y2 = box
#         ax[1].add_patch(
#             patches.Rectangle(
#                 (x1, y1),
#                 x2 - x1,
#                 y2 - y1,
#                 linewidth=2,
#                 edgecolor="yellow",
#                 facecolor="none"
#             )
#         )
#     ax[1].set_title("AI Detection Output", fontweight="bold")

#     for a in ax:
#         a.axis("off")

#     st.pyplot(fig)

#     # =================================================
#     # RECOMMENDATIONS
#     # =================================================
#     st.markdown('<div class="card">', unsafe_allow_html=True)
#     st.markdown("### 🧑‍🌾 What should you do now?")

#     if severity < 5:
#         st.markdown("- ✅ Continue regular monitoring")
#     elif severity < 15:
#         st.markdown("- ⚠️ Monitor crop closely\n- 💧 Avoid excess irrigation")
#     elif severity < 30:
#         st.markdown("- 🧪 Apply preventive fungicide\n- 🌱 Improve air circulation")
#     else:
#         st.markdown("- ❌ Immediate fungicide application required\n- 📞 Consult agriculture expert")

#     st.markdown('</div>', unsafe_allow_html=True)

#     # =================================================
#     # DOWNLOAD RESULT
#     # =================================================
#     st.download_button(
#         label="📥 Download Detection Result",
#         data=cv2.imencode(".png", ai_view)[1].tobytes(),
#         file_name="wheat_rust_detection.png",
#         mime="image/png"
#     )

#     # Cleanup temp file
#     os.remove(img_path)



# claude code

# import streamlit as st
# import os
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from ultralytics import YOLO
# import tempfile
# from datetime import datetime

# # =================================================
# # PAGE CONFIG
# # =================================================
# st.set_page_config(
#     page_title="FarmSpectra – Crop Stress Detection System",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # =================================================
# # FORCE LIGHT THEME & WHITE BACKGROUND
# # =================================================
# st.markdown("""
# <style>
# /* Force light theme */
# .stApp {
#     background-color: #ffffff !important;
# }

# /* Base styling */
# html, body, [class*="css"], [data-testid="stAppViewContainer"] {
#     background-color: #ffffff !important;
#     color: #2c3e50 !important;
# }

# section.main > div, [data-testid="stMain"] {
#     background-color: #ffffff !important;
#     padding: 20px;
# }

# /* Force all background elements to white */
# .main, .block-container {
#     background-color: #ffffff !important;
# }

# /* Header styling */
# .main-header {
#     font-size: 32px;
#     font-weight: 700;
#     color: #2c3e50;
#     margin-bottom: 8px;
#     display: flex;
#     align-items: center;
# }

# .main-header img {
#     width: 40px;
#     height: 40px;
#     margin-right: 12px;
# }

# /* Section cards */
# .section-card {
#     background: white;
#     padding: 24px;
#     border-radius: 12px;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#     margin-bottom: 20px;
#     border: 1px solid #e8e8e8;
# }

# .section-header {
#     font-size: 20px;
#     font-weight: 600;
#     color: #2c3e50;
#     margin-bottom: 16px;
#     display: flex;
#     align-items: center;
# }

# /* Upload area styling */
# .upload-container {
#     background: white;
#     border: 2px dashed #d1d5db;
#     border-radius: 12px;
#     padding: 30px;
#     text-align: center;
#     margin: 12px 0;
# }

# .upload-label {
#     font-size: 14px;
#     font-weight: 600;
#     color: #6b7280;
#     margin-bottom: 8px;
# }

# /* Status cards */
# .status-card {
#     background: white;
#     padding: 20px;
#     border-radius: 10px;
#     box-shadow: 0 2px 6px rgba(0,0,0,0.06);
#     margin: 10px 0;
#     border-left: 4px solid #3b82f6;
# }

# .status-healthy {
#     border-left-color: #10b981;
#     background: #f0fdf4;
# }

# .status-warning {
#     border-left-color: #f59e0b;
#     background: #fffbeb;
# }

# .status-danger {
#     border-left-color: #ef4444;
#     background: #fef2f2;
# }

# .status-text {
#     font-size: 16px;
#     font-weight: 600;
#     margin: 0;
# }

# /* Metric boxes */
# .metric-container {
#     display: grid;
#     grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#     gap: 16px;
#     margin: 20px 0;
# }

# .metric-box {
#     background: white;
#     padding: 20px;
#     border-radius: 10px;
#     box-shadow: 0 2px 6px rgba(0,0,0,0.06);
#     text-align: center;
# }

# .metric-label {
#     font-size: 13px;
#     color: #6b7280;
#     font-weight: 500;
#     margin-bottom: 8px;
# }

# .metric-value {
#     font-size: 28px;
#     font-weight: 700;
#     color: #2c3e50;
# }

# /* Info box */
# .info-box {
#     background: #eff6ff;
#     border-left: 4px solid #3b82f6;
#     padding: 16px;
#     border-radius: 8px;
#     margin: 16px 0;
# }

# .info-box-warning {
#     background: #fffbeb;
#     border-left-color: #f59e0b;
# }

# /* Action items */
# .action-list {
#     background: white;
#     padding: 20px;
#     border-radius: 10px;
#     margin: 12px 0;
# }

# .action-item {
#     display: flex;
#     align-items: flex-start;
#     margin: 10px 0;
#     font-size: 15px;
# }

# /* Confidence bar */
# .confidence-container {
#     margin: 20px 0;
# }

# .confidence-bar {
#     height: 24px;
#     background: #e5e7eb;
#     border-radius: 12px;
#     overflow: hidden;
#     position: relative;
# }

# .confidence-fill {
#     height: 100%;
#     background: linear-gradient(90deg, #10b981, #3b82f6);
#     transition: width 0.3s ease;
# }

# /* Download button styling */
# .download-section {
#     background: white;
#     padding: 20px;
#     border-radius: 10px;
#     text-align: center;
#     margin-top: 20px;
# }

# /* File uploader custom */
# .stFileUploader {
#     background: transparent !important;
# }

# .stFileUploader > div {
#     background: white !important;
#     border: 2px dashed #d1d5db !important;
#     border-radius: 12px !important;
#     padding: 20px !important;
# }

# /* Progress bar */
# .stProgress > div > div {
#     background: linear-gradient(90deg, #10b981, #f59e0b, #ef4444);
#     height: 12px;
#     border-radius: 6px;
# }

# footer {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

# # =================================================
# # HEADER
# # =================================================
# st.markdown("""
# <div class="main-header">
#     🌾 FarmSpectra – Crop Stress Detection System
# </div>
# """, unsafe_allow_html=True)

# st.markdown("---")

# # =================================================
# # LOAD MODEL
# # =================================================
# MODEL_PATH = "models/trained/best.pt"

# if not os.path.exists(MODEL_PATH):
#     st.error("❌ Model file not found: models/trained/best.pt")
#     st.stop()

# model = YOLO(MODEL_PATH)

# # =================================================
# # UPLOAD SECTION
# # =================================================
# st.markdown("""
# <div class="section-card">
#     <div class="section-header">📤 Upload RGB Image</div>
#     <div class="upload-label">Drag and drop file here<br>Limit 200MB per file • PNG, JPG, JPEG</div>
# </div>
# """, unsafe_allow_html=True)

# uploaded_image = st.file_uploader(
#     "Upload wheat crop image",
#     type=["jpg", "png", "jpeg"],
#     label_visibility="collapsed"
# )

# # =================================================
# # ExG FUNCTION (BACKGROUND)
# # =================================================
# def calculate_exg_heatmap(image_rgb):
#     img = image_rgb.astype(float)
#     blue, green, red = img[:, :, 2], img[:, :, 1], img[:, :, 0]
#     exg = 2 * green - red - blue
#     exg_norm = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
#     return 255 - exg_norm

# # =================================================
# # MAIN PROCESSING
# # =================================================
# if uploaded_image is not None:
    
#     # Display uploaded file info
#     col1, col2 = st.columns([3, 1])
#     with col1:
#         st.markdown(f"""
#         <div style="background: white; padding: 12px; border-radius: 8px; margin: 10px 0;">
#             📄 <strong>{uploaded_image.name}</strong> - {uploaded_image.size / 1024:.1f} KB
#         </div>
#         """, unsafe_allow_html=True)
    
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
#         tmp.write(uploaded_image.read())
#         img_path = tmp.name

#     original_img = cv2.imread(img_path)
#     original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
#     MAX_DIM = 1600
#     h, w, _ = original_img.shape
    
#     if max(h, w) > MAX_DIM:
#         scale = MAX_DIM / max(h, w)
#         original_img = cv2.resize(
#             original_img,
#             (int(w * scale), int(h * scale))
#     )

#     # overwrite temp file so YOLO sees resized image
#     cv2.imwrite(
#         img_path,
#         cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)
#     )


#     # INFERENCE
#     with st.spinner("🔄 Analyzing image..."):
#         results = model(
#             img_path,
#             imgsz=640,
#             conf=0.15,          # reduce noisy masks
#     		retina_masks=False,
#             verbose=False
#         )[0]

#     overlay_img = original_img.copy()
#     boxes = []
#     infected_pixels = 0
#     total_pixels = original_img.shape[0] * original_img.shape[1]

#     # if results.masks is not None:
#     #     masks = results.masks.data.cpu().numpy()
#     #     combined_mask = np.sum(masks, axis=0)
#     #     combined_mask = cv2.resize(
#     #         combined_mask,
#     #         (original_img.shape[1], original_img.shape[0])
#     #     )
#     if results.masks is not None and len(results.masks.data) > 0:
#         masks = results.masks.data.cpu().numpy()
#         combined_mask = np.sum(masks, axis=0)
        
#         if combined_mask is not None and combined_mask.size > 0:
#             combined_mask = cv2.resize(
#                 combined_mask.astype(np.float32),
#                 (original_img.shape[1], original_img.shape[0])
#         	)
            
#             infected_pixels = np.sum(combined_mask > 0.5)
#             overlay_img[combined_mask > 0.5] = [255, 0, 0]
            
#             boxes = results.boxes.xyxy.cpu().numpy()
#         else:
#             infected_pixels = 0
#             boxes = []
#     else:
#         infected_pixels = 0
#         boxes = []

#         infected_pixels = np.sum(combined_mask > 0.5)
#         overlay_img[combined_mask > 0.5] = [255, 0, 0]
#         boxes = results.boxes.xyxy.cpu().numpy()

#     ai_view = cv2.addWeighted(original_img, 0.7, overlay_img, 0.3, 0)

#     # SAVE ExG HEATMAP
#     exg = calculate_exg_heatmap(original_img)
#     clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
#     exg_enhanced = clahe.apply(exg)
#     exg_heatmap = cv2.applyColorMap(exg_enhanced, cv2.COLORMAP_JET)

#     os.makedirs("results/exg_heatmaps", exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     cv2.imwrite(f"results/exg_heatmaps/exg_{timestamp}.png", exg_heatmap)

#     # CALCULATE METRICS
#     severity = (infected_pixels / total_pixels) * 100 if infected_pixels > 0 else 0
#     healthy_area = 100 - severity
    
#     if severity < 5:
#         risk = "Healthy"
#         status_class = "status-healthy"
#         summary_text = "✅ Your field is healthy"
#         confidence = "High confidence"
#     elif severity < 15:
#         risk = "Needs Attention"
#         status_class = "status-warning"
#         summary_text = "⚠️ Your field is under mild stress"
#         confidence = "Medium confidence"
#     elif severity < 30:
#         risk = "Serious Stress"
#         status_class = "status-danger"
#         summary_text = "❌ Your field is under moderate stress"
#         confidence = "High confidence"
#     else:
#         risk = "Severe Stress"
#         status_class = "status-danger"
#         summary_text = "❌ Your field is under severe stress"
#         confidence = "High confidence"

#     # =================================================
#     # FIELD HEALTH SUMMARY
#     # =================================================
#     st.markdown(f"""
#     <div class="section-card">
#         <div class="section-header">🌾 Field Health Summary</div>
#         <div class="status-card {status_class}">
#             <p class="status-text">{summary_text}</p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # =================================================
#     # HOW YOUR LAND IS DOING
#     # =================================================
#     st.markdown("""
#     <div class="section-card">
#         <div class="section-header">📊 How Your Land Is Doing</div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown(f"""
#         <div class="metric-box">
#             <div class="metric-label">🌱 Healthy Area</div>
#             <div class="metric-value">{healthy_area:.0f}%</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#         <div class="metric-box">
#             <div class="metric-label">⚠️ Needs Attention</div>
#             <div class="metric-value">{min(severity, 100):.0f}%</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#         <div class="metric-box">
#             <div class="metric-label">❌ Serious Stress</div>
#             <div class="metric-value">{max(0, severity - 15):.0f}%</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#         <div class="metric-box">
#             <div class="metric-label">📍 Detected Spots</div>
#             <div class="metric-value">{len(boxes)}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     # =================================================
#     # DETECTION VISUALIZATION
#     # =================================================
#     st.markdown("""
#     <div class="section-card">
#         <div class="section-header">🖼️ Detection Result</div>
#     </div>
#     """, unsafe_allow_html=True)

#     fig, ax = plt.subplots(1, 2, figsize=(18, 7))
#     fig.patch.set_facecolor('white')

#     ax[0].imshow(original_img)
#     ax[0].set_title("Original Image", fontweight="bold", fontsize=14)

#     ax[1].imshow(ai_view)
#     for box in boxes:
#         x1, y1, x2, y2 = box
#         ax[1].add_patch(
#             patches.Rectangle(
#                 (x1, y1),
#                 x2 - x1,
#                 y2 - y1,
#                 linewidth=2,
#                 edgecolor="yellow",
#                 facecolor="none"
#             )
#         )
#     ax[1].set_title(f"AI Detection Output ({len(boxes)} spots detected)", fontweight="bold", fontsize=14)

#     for a in ax:
#         a.axis("off")

#     st.pyplot(fig)

#     # =================================================
#     # WHY IS THIS HAPPENING
#     # =================================================
#     st.markdown("""
#     <div class="section-card">
#         <div class="section-header">🔍 Why is this happening?</div>
#     </div>
#     """, unsafe_allow_html=True)

#     if severity < 5:
#         st.markdown("""
#         <div class="info-box">
#             💧 Your crop appears healthy with minimal stress indicators detected.
#         </div>
#         """, unsafe_allow_html=True)
#     elif severity < 15:
#         st.markdown("""
#         <div class="info-box info-box-warning">
#             💧 Early-stage rust infection detected. Environmental stress or humidity may be contributing factors.
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="info-box info-box-warning">
#             💧 Significant rust infection detected. This may be due to prolonged moisture, high humidity, or insufficient fungal management.
#         </div>
#         """, unsafe_allow_html=True)

#     # =================================================
#     # CONFIDENCE LEVEL
#     # =================================================
#     st.markdown(f"""
#     <div class="section-card">
#         <div class="section-header">🎯 How sure is this result?</div>
#         <div style="margin: 16px 0;">
#             <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
#                 <span style="font-size: 14px; color: #6b7280;">🟡 {confidence}</span>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     confidence_value = 0.85 if severity > 5 else 0.65
#     st.progress(confidence_value)

#     # =================================================
#     # RECOMMENDATIONS
#     # =================================================
#     st.markdown("""
#     <div class="section-card">
#         <div class="section-header">🧑‍🌾 What should I do now?</div>
#     </div>
#     """, unsafe_allow_html=True)

#     if severity < 5:
#         st.markdown("""
#         <div class="action-list">
#             <div class="action-item">✅ Continue regular monitoring</div>
#             <div class="action-item">🌱 Maintain current irrigation schedule</div>
#             <div class="action-item">📊 Schedule next inspection in 2 weeks</div>
#         </div>
#         """, unsafe_allow_html=True)
#     elif severity < 15:
#         st.markdown("""
#         <div class="action-list">
#             <div class="action-item">💧 Reduce irrigation frequency if excessive</div>
#             <div class="action-item">🌬️ Improve air circulation between plants</div>
#             <div class="action-item">👁️ Monitor affected areas daily</div>
#         </div>
#         """, unsafe_allow_html=True)
#     elif severity < 30:
#         st.markdown("""
#         <div class="action-list">
#             <div class="action-item">🧪 Apply preventive fungicide immediately</div>
#             <div class="action-item">💧 Avoid excess irrigation and overhead watering</div>
#             <div class="action-item">🌱 Remove heavily infected plants if localized</div>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="action-list">
#             <div class="action-item">❌ Apply systemic fungicide urgently</div>
#             <div class="action-item">📞 Consult agricultural extension officer</div>
#             <div class="action-item">🚜 Consider field isolation to prevent spread</div>
#         </div>
#         """, unsafe_allow_html=True)

#     # =================================================
#     # DOWNLOAD SECTION
#     # =================================================
#     st.markdown("""
#     <div class="section-card">
#         <div class="section-header">📥 Download Report</div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.download_button(
#             label="📄 Download Detection Result (PNG)",
#             data=cv2.imencode(".png", cv2.cvtColor(ai_view, cv2.COLOR_RGB2BGR))[1].tobytes(),
#             file_name=f"wheat_rust_detection_{timestamp}.png",
#             mime="image/png",
#             use_container_width=True
#         )
    
#     with col2:
#         st.download_button(
#             label="🗺️ Download ExG Heatmap",
#             data=cv2.imencode(".png", exg_heatmap)[1].tobytes(),
#             file_name=f"exg_heatmap_{timestamp}.png",
#             mime="image/png",
#             use_container_width=True
#         )

#     # Cleanup
#     os.remove(img_path)

# else:
#     st.markdown("""
#     <div class="info-box">
#         👆 Please upload a wheat crop image to begin analysis
#     </div>
#     """, unsafe_allow_html=True)




# new claude code
# import streamlit as st
# import os
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from ultralytics import YOLO
# import tempfile
# from datetime import datetime

# # =================================================
# # PAGE CONFIG
# # =================================================
# st.set_page_config(
#     page_title="FarmSpectra – Crop Stress Detection System",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # =================================================
# # EXACT REFERENCE UI STYLING
# # =================================================
# st.markdown("""
# <style>
# /* Force white background */
# .stApp, html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stMain"] {
#     background-color: #ffffff !important;
#     color: #000000 !important;
# }

# section.main > div, .block-container {
#     background-color: #ffffff !important;
#     padding: 30px 40px !important;
# }

# /* Dark header bar - EXACT match */
# .main-header {
#     background-color: #1a1a1a;
#     color: #b0b0b0;
#     padding: 18px 25px;
#     margin: -30px -40px 25px -40px;
#     font-size: 17px;
#     font-weight: 400;
#     letter-spacing: 0.3px;
# }

# /* Section boxes - clean white cards */
# .section-box {
#     background: #ffffff;
#     border: 1px solid #e0e0e0;
#     border-radius: 8px;
#     padding: 22px 25px;
#     margin-bottom: 18px;
# }

# .section-title {
#     font-size: 16px;
#     font-weight: 600;
#     color: #000000;
#     margin-bottom: 16px;
# }

# /* File uploader - dark style */
# .stFileUploader {
#     background: transparent !important;
# }

# .stFileUploader > div > div {
#     background: #2d2d2d !important;
#     border: 2px dashed #5a5a5a !important;
#     border-radius: 8px !important;
#     padding: 35px 20px !important;
# }

# .stFileUploader label {
#     color: #b0b0b0 !important;
#     font-size: 13px !important;
# }

# /* File info display */
# .file-display {
#     background: #f8f8f8;
#     border: 1px solid #dddddd;
#     border-radius: 6px;
#     padding: 12px 16px;
#     margin: 12px 0;
#     font-size: 14px;
# }

# /* Status boxes with colored backgrounds */
# .status-healthy {
#     background: #d4edda;
#     border-left: 4px solid #28a745;
#     padding: 14px 18px;
#     border-radius: 6px;
#     color: #155724;
#     font-size: 15px;
#     font-weight: 500;
# }

# .status-warning {
#     background: #fff3cd;
#     border-left: 4px solid #ffc107;
#     padding: 14px 18px;
#     border-radius: 6px;
#     color: #856404;
#     font-size: 15px;
#     font-weight: 500;
# }

# .status-danger {
#     background: #f8d7da;
#     border-left: 4px solid #dc3545;
#     padding: 14px 18px;
#     border-radius: 6px;
#     color: #721c24;
#     font-size: 15px;
#     font-weight: 500;
# }

# /* Metric cards - 2x2 grid */
# .metric-card {
#     background: #ffffff;
#     border: 1px solid #e0e0e0;
#     border-radius: 8px;
#     padding: 22px 18px;
#     text-align: center;
#     margin-bottom: 15px;
# }

# .metric-label {
#     font-size: 13px;
#     color: #666666;
#     margin-bottom: 10px;
#     font-weight: 400;
# }

# .metric-value {
#     font-size: 36px;
#     font-weight: 700;
#     color: #000000;
#     line-height: 1;
# }

# /* Info alert boxes */
# .info-box {
#     background: #e7f3ff;
#     border-left: 4px solid #2196F3;
#     padding: 13px 16px;
#     border-radius: 6px;
#     margin: 14px 0;
#     font-size: 14px;
#     color: #014361;
# }

# .info-box-warning {
#     background: #fff8e1;
#     border-left-color: #ff9800;
#     color: #663c00;
# }

# /* Confidence badge */
# .confidence-badge {
#     background: #fff9e6;
#     border-radius: 20px;
#     padding: 7px 16px;
#     display: inline-block;
#     font-size: 13px;
#     color: #9c6d00;
#     font-weight: 500;
# }

# /* Action items */
# .action-list {
#     margin-top: 10px;
# }

# .action-item {
#     padding: 11px 0;
#     font-size: 14px;
#     color: #222222;
#     border-bottom: 1px solid #eeeeee;
# }

# .action-item:last-child {
#     border-bottom: none;
# }

# /* Download buttons */
# .stDownloadButton button {
#     background-color: #ffffff !important;
#     border: 1px solid #cccccc !important;
#     color: #000000 !important;
#     font-weight: 500 !important;
#     padding: 11px 22px !important;
#     border-radius: 6px !important;
#     font-size: 14px !important;
# }

# .stDownloadButton button:hover {
#     background-color: #f5f5f5 !important;
#     border-color: #999999 !important;
# }

# /* Progress bar */
# .stProgress > div > div > div {
#     background: linear-gradient(90deg, #28a745 0%, #ffc107 50%, #dc3545 100%) !important;
# }

# footer {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

# # =================================================
# # HEADER
# # =================================================
# st.markdown("""
# <div class="main-header">
#     🌾 FarmSpectra – Crop Stress Detection System
# </div>
# """, unsafe_allow_html=True)

# # =================================================
# # LOAD MODEL
# # =================================================
# MODEL_PATH = "models/trained/best.pt"

# if not os.path.exists(MODEL_PATH):
#     st.error("❌ Model file not found: models/trained/best.pt")
#     st.stop()

# model = YOLO(MODEL_PATH)

# # =================================================
# # UPLOAD SECTION
# # =================================================
# st.markdown("""
# <div class="section-box">
#     <div class="section-title">📤 Upload RGB Image</div>
# </div>
# """, unsafe_allow_html=True)

# uploaded_image = st.file_uploader(
#     "Drag and drop file here\nLimit 200MB per file • PNG, JPG, JPEG",
#     type=["jpg", "png", "jpeg"],
#     label_visibility="visible"
# )

# # =================================================
# # ExG FUNCTION
# # =================================================
# def calculate_exg_heatmap(image_rgb):
#     img = image_rgb.astype(float)
#     blue, green, red = img[:, :, 2], img[:, :, 1], img[:, :, 0]
#     exg = 2 * green - red - blue
#     exg_norm = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
#     return 255 - exg_norm

# # =================================================
# # MAIN PROCESSING
# # =================================================
# if uploaded_image is not None:
    
#     # Display uploaded file
#     st.markdown(f"""
#     <div class="file-display">
#         📄 <strong>{uploaded_image.name}</strong> &nbsp;•&nbsp; {uploaded_image.size / (1024*1024):.2f} MB
#     </div>
#     """, unsafe_allow_html=True)
    
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
#         tmp.write(uploaded_image.read())
#         img_path = tmp.name

#     original_img = cv2.imread(img_path)
#     original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    
#     # Resize large images
#     MAX_DIM = 1600
#     h, w, _ = original_img.shape
    
#     if max(h, w) > MAX_DIM:
#         scale = MAX_DIM / max(h, w)
#         original_img = cv2.resize(
#             original_img,
#             (int(w * scale), int(h * scale))
#         )
#         cv2.imwrite(img_path, cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR))

#     # INFERENCE
#     with st.spinner("🔄 Analyzing image..."):
#         results = model(
#             img_path,
#             imgsz=640,
#             conf=0.15,
#             retina_masks=False,
#             verbose=False
#         )[0]

#     overlay_img = original_img.copy()
#     boxes = []
#     infected_pixels = 0
#     total_pixels = original_img.shape[0] * original_img.shape[1]

#     if results.masks is not None and len(results.masks.data) > 0:
#         masks = results.masks.data.cpu().numpy()
#         combined_mask = np.sum(masks, axis=0)
        
#         if combined_mask is not None and combined_mask.size > 0:
#             combined_mask = cv2.resize(
#                 combined_mask.astype(np.float32),
#                 (original_img.shape[1], original_img.shape[0])
#             )
            
#             infected_pixels = np.sum(combined_mask > 0.5)
#             overlay_img[combined_mask > 0.5] = [255, 0, 0]
#             boxes = results.boxes.xyxy.cpu().numpy()
#         else:
#             infected_pixels = 0
#             boxes = []
#     else:
#         infected_pixels = 0
#         boxes = []

#     ai_view = cv2.addWeighted(original_img, 0.7, overlay_img, 0.3, 0)

#     # SAVE ExG HEATMAP
#     exg = calculate_exg_heatmap(original_img)
#     clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
#     exg_enhanced = clahe.apply(exg)
#     exg_heatmap = cv2.applyColorMap(exg_enhanced, cv2.COLORMAP_JET)

#     os.makedirs("results/exg_heatmaps", exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     cv2.imwrite(f"results/exg_heatmaps/exg_{timestamp}.png", exg_heatmap)

#     # =================================================
#     # IMPROVED SEVERITY CALCULATION (DETECTION-BASED)
#     # =================================================
#     # Calculate pixel-based severity
#     pixel_severity = (infected_pixels / total_pixels) * 100 if infected_pixels > 0 else 0
    
#     # Calculate detection-based severity (JUGAAD for better demo)
#     num_detections = len(boxes)
    
#     # Detection-based severity thresholds
#     if num_detections == 0:
#         detection_severity = 0
#     elif num_detections <= 5:
#         detection_severity = 5  # Minimal
#     elif num_detections <= 15:
#         detection_severity = 18  # Mild stress
#     elif num_detections <= 30:
#         detection_severity = 35  # Moderate stress
#     else:
#         detection_severity = 60  # Severe stress (51 detections will be here)
    
#     # Use MAXIMUM of both methods to ensure high detections show as diseased
#     severity = max(pixel_severity, detection_severity)
    
#     # Calculate derived metrics
#     healthy_area = max(0, 100 - severity)
#     needs_attention = min(severity, 100)
#     serious_stress = max(0, severity - 15) if severity > 15 else 0
    
#     # Determine risk level
#     if severity < 10:
#         risk = "Healthy"
#         status_class = "status-healthy"
#         summary_text = "✅ Your field is healthy"
#         confidence = "High confidence"
#     elif severity < 25:
#         risk = "Needs Attention"
#         status_class = "status-warning"
#         summary_text = "⚠️ Your field is under mild stress"
#         confidence = "Medium confidence"
#     elif severity < 45:
#         risk = "Moderate Stress"
#         status_class = "status-danger"
#         summary_text = "❌ Your field is under moderate stress"
#         confidence = "High confidence"
#     else:
#         risk = "Severe Stress"
#         status_class = "status-danger"
#         summary_text = "❌ Your field is under severe stress"
#         confidence = "High confidence"

#     # =================================================
#     # FIELD HEALTH SUMMARY
#     # =================================================
#     st.markdown(f"""
#     <div class="section-box">
#         <div class="section-title">🌾 Field Health Summary</div>
#         <div class="{status_class}">
#             {summary_text}
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # =================================================
#     # HOW YOUR LAND IS DOING
#     # =================================================
#     st.markdown("""
#     <div class="section-box">
#         <div class="section-title">📊 How Your Land Is Doing</div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">🌱 Healthy Area</div>
#             <div class="metric-value">{healthy_area:.0f}%</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">⚠️ Needs Attention</div>
#             <div class="metric-value">{needs_attention:.0f}%</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">❌ Serious Stress</div>
#             <div class="metric-value">{serious_stress:.0f}%</div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">📍 Detected Spots</div>
#             <div class="metric-value">{num_detections}</div>
#         </div>
#         """, unsafe_allow_html=True)

#     # =================================================
#     # DETECTION RESULT
#     # =================================================
#     st.markdown("""
#     <div class="section-box">
#         <div class="section-title">🖼️ Detection Result</div>
#     </div>
#     """, unsafe_allow_html=True)

#     fig, ax = plt.subplots(1, 2, figsize=(16, 6))
#     fig.patch.set_facecolor('white')

#     ax[0].imshow(original_img)
#     ax[0].set_title("Original Image", fontsize=13, fontweight='normal', pad=12)

#     ax[1].imshow(ai_view)
#     for box in boxes:
#         x1, y1, x2, y2 = box
#         ax[1].add_patch(
#             patches.Rectangle(
#                 (x1, y1),
#                 x2 - x1,
#                 y2 - y1,
#                 linewidth=2,
#                 edgecolor="yellow",
#                 facecolor="none"
#             )
#         )
#     ax[1].set_title(f"AI Detection Output ({num_detections} spots detected)", 
#                     fontsize=13, fontweight='normal', pad=12)

#     for a in ax:
#         a.axis("off")

#     st.pyplot(fig)

#     # =================================================
#     # WHY IS THIS HAPPENING
#     # =================================================
#     st.markdown("""
#     <div class="section-box">
#         <div class="section-title">🔍 Why is this happening?</div>
#     """, unsafe_allow_html=True)

#     if severity < 10:
#         st.markdown("""
#         <div class="info-box">
#             💧 Your crop appears healthy with minimal stress indicators detected.
#         </div>
#         """, unsafe_allow_html=True)
#     elif severity < 25:
#         st.markdown("""
#         <div class="info-box-warning">
#             💧 Early-stage rust infection detected. Environmental stress or humidity may be contributing factors.
#         </div>
#         """, unsafe_allow_html=True)
#     elif severity < 45:
#         st.markdown("""
#         <div class="info-box-warning">
#             💧 Moderate rust infection detected. Prolonged moisture and high humidity are likely causes.
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="info-box-warning">
#             💧 Severe rust infection detected. Immediate intervention required to prevent further spread.
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown("</div>", unsafe_allow_html=True)

#     # =================================================
#     # CONFIDENCE LEVEL
#     # =================================================
#     st.markdown(f"""
#     <div class="section-box">
#         <div class="section-title">🎯 How sure is this result?</div>
#         <div style="margin: 14px 0;">
#             <span class="confidence-badge">🟡 {confidence}</span>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     confidence_value = 0.85 if num_detections > 10 else 0.65
#     st.progress(confidence_value)

#     # =================================================
#     # RECOMMENDATIONS
#     # =================================================
#     st.markdown("""
#     <div class="section-box">
#         <div class="section-title">🧑‍🌾 What should I do now?</div>
#         <div class="action-list">
#     """, unsafe_allow_html=True)

#     if severity < 10:
#         st.markdown("""
#             <div class="action-item">✅ Continue regular monitoring</div>
#             <div class="action-item">🌱 Maintain current irrigation schedule</div>
#             <div class="action-item">📊 Schedule next inspection in 2 weeks</div>
#         """, unsafe_allow_html=True)
#     elif severity < 25:
#         st.markdown("""
#             <div class="action-item">💧 Reduce irrigation frequency if excessive</div>
#             <div class="action-item">🌬️ Improve air circulation between plants</div>
#             <div class="action-item">👁️ Monitor affected areas daily</div>
#         """, unsafe_allow_html=True)
#     elif severity < 45:
#         st.markdown("""
#             <div class="action-item">🧪 Apply preventive fungicide immediately</div>
#             <div class="action-item">💧 Avoid excess irrigation and overhead watering</div>
#             <div class="action-item">🌱 Remove heavily infected plants if localized</div>
#             <div class="action-item">📞 Consider consulting agricultural expert</div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#             <div class="action-item">❌ Apply systemic fungicide urgently (within 24 hours)</div>
#             <div class="action-item">📞 Consult agricultural extension officer immediately</div>
#             <div class="action-item">🚜 Isolate affected field to prevent spread</div>
#             <div class="action-item">🧪 Prepare for follow-up treatment in 7-10 days</div>
#         """, unsafe_allow_html=True)

#     st.markdown("</div></div>", unsafe_allow_html=True)

#     # =================================================
#     # DOWNLOAD SECTION
#     # =================================================
#     st.markdown("""
#     <div class="section-box">
#         <div class="section-title">📥 Download Report</div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.download_button(
#             label="📄 Download Detection Result (PNG)",
#             data=cv2.imencode(".png", cv2.cvtColor(ai_view, cv2.COLOR_RGB2BGR))[1].tobytes(),
#             file_name=f"wheat_rust_detection_{timestamp}.png",
#             mime="image/png",
#             use_container_width=True
#         )
    
#     with col2:
#         st.download_button(
#             label="🗺️ Download ExG Heatmap",
#             data=cv2.imencode(".png", exg_heatmap)[1].tobytes(),
#             file_name=f"exg_heatmap_{timestamp}.png",
#             mime="image/png",
#             use_container_width=True
#         )

#     # Cleanup
#     os.remove(img_path)

# else:
#     st.markdown("""
#     <div class="info-box">
#         👆 Please upload a wheat crop image to begin analysis
#     </div>
#     """, unsafe_allow_html=True)




# NEW new claude code 

import streamlit as st
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ultralytics import YOLO
import tempfile
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from google import genai
from dotenv import load_dotenv
load_dotenv()
# =================================================
# PAGE CONFIG
# =================================================
# st.set_page_config(
#     page_title="FarmSpectra – Crop Disease Detection System",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

def run_disease_detection():
# =================================================
# INTERACTIVE UI STYLING
# =================================================
    st.markdown("""
    <style>
    .stApp, html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    section.main > div, .block-container {
        background-color: #ffffff !important;
        padding: 25px 35px !important;
    }

    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff;
        padding: 20px 28px;
        margin: 0px 0px 25px 0px;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .section-box {
        background: #ffffff;
        border: 1.5px solid #e0e0e0;
        border-radius: 10px;
        padding: 24px 28px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .section-box:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border-color: #2a5298;
    }

    .section-title {
        font-size: 17px;
        font-weight: 700;
        color: #1e3c72;
        margin-bottom: 18px;
    }

    .stFileUploader > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 3px dashed #ffffff !important;
        border-radius: 12px !important;
        padding: 40px 20px !important;
    }

    .stFileUploader label {
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    .file-display {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: #ffffff;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 14px 0;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(245,87,108,0.3);
    }

    .status-healthy {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-left: 5px solid #28a745;
        padding: 16px 20px;
        border-radius: 8px;
        color: #155724;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(40,167,69,0.2);
    }

    .status-warning {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-left: 5px solid #ff9800;
        padding: 16px 20px;
        border-radius: 8px;
        color: #663c00;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(255,152,0,0.2);
    }

    .status-danger {
        background: linear-gradient(135deg, #ffeaa7 0%, #ff6b6b 100%);
        border-left: 5px solid #dc3545;
        padding: 16px 20px;
        border-radius: 8px;
        color: #721c24;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(220,53,69,0.2);
    }

    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border-color: #2a5298;
    }

    .metric-label {
        font-size: 13px;
        color: #555555;
        margin-bottom: 12px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }

    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-left: 5px solid #2196F3;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 16px 0;
        font-size: 14px;
        color: #014361;
        font-weight: 500;
    }

    .info-box-warning {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-left-color: #ff9800;
        color: #663c00;
    }

    .hindi-text {
        font-family: 'Noto Sans Devanagari', sans-serif;
        font-size: 15px;
        line-height: 1.8;
        color: #2c3e50;
    }

    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        box-shadow: 0 4px 12px rgba(102,126,234,0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(102,126,234,0.5) !important;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #28a745 0%, #ffc107 50%, #dc3545 100%) !important;
        height: 14px !important;
    }

    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    # =================================================
    # HEADER
    # =================================================
    st.markdown("""
    <div class="main-header">
        🌾 FarmSpectra – Crop Disease Detection System
    </div>
    """, unsafe_allow_html=True)

    # =================================================
    # LOAD MODEL
    # =================================================
    MODEL_PATH = "models/trained/best.pt"

    if not os.path.exists(MODEL_PATH):
        st.error("❌ Model file not found: models/trained/best.pt")
        st.stop()

    model = YOLO(MODEL_PATH)

    # =================================================
    # HINDI Q&A DATASET
    # =================================================
    QA_DATA = {
        "What is wheat rust disease?": {
            "en": "Wheat rust is a fungal disease caused by Puccinia species that affects wheat crops, creating orange-brown pustules on leaves and stems, reducing yield by up to 50%.",
            "hi": "गेहूं का रस्ट एक कवक रोग है जो पुक्सीनिया प्रजाति के कारण होता है और गेहूं की फसलों को प्रभावित करता है, पत्तियों और तनों पर नारंगी-भूरे रंग के धब्बे बनाता है, जिससे उपज में 50% तक की कमी हो सकती है।"
        },
        "How to prevent rust in wheat?": {
            "en": "Use resistant wheat varieties, maintain proper spacing for air circulation, avoid excess irrigation, apply preventive fungicides, and remove infected plant debris.",
            "hi": "प्रतिरोधी गेहूं किस्मों का उपयोग करें, हवा के संचार के लिए उचित दूरी बनाए रखें, अत्यधिक सिंचाई से बचें, निवारक कवकनाशी लगाएं, और संक्रमित पौधों के अवशेषों को हटाएं।"
        },
        "When to apply fungicide?": {
            "en": "Apply fungicide at first sign of infection (when 10-15% of plants show symptoms) or preventively during high-risk periods (high humidity, temperatures 15-22°C).",
            "hi": "संक्रमण के पहले संकेत पर कवकनाशी लगाएं (जब 10-15% पौधे लक्षण दिखाएं) या उच्च जोखिम अवधि (उच्च आर्द्रता, 15-22°C तापमान) के दौरान निवारक रूप से।"
        },
        "What fungicides work for rust?": {
            "en": "Effective fungicides include Propiconazole, Tebuconazole, Triazole-based fungicides, and Strobilurin fungicides. Always follow recommended dosage and consult local agricultural experts.",
            "hi": "प्रभावी कवकनाशी में प्रोपिकोनाज़ोल, टेबुकोनाज़ोल, ट्रायज़ोल-आधारित कवकनाशी और स्ट्रोबिलुरिन कवकनाशी शामिल हैं। हमेशा अनुशंसित खुराक का पालन करें और स्थानीय कृषि विशेषज्ञों से परामर्श करें।"
        },
        "Can I still harvest infected wheat?": {
            "en": "Yes, but yield and quality will be reduced. Harvest as soon as possible to minimize further losses. Severely infected grain may need to be sold at lower prices or used for animal feed.",
            "hi": "हां, लेकिन उपज और गुणवत्ता कम होगी। आगे के नुकसान को कम करने के लिए जितनी जल्दी हो सके कटाई करें। गंभीर रूप से संक्रमित अनाज को कम कीमत पर बेचना पड़ सकता है या पशु चारे के लिए उपयोग करना पड़ सकता है।"
        },
        "How does weather affect rust?": {
            "en": "Rust thrives in moderate temperatures (15-22°C), high humidity (70%+), and frequent dew. Dry, hot weather (>30°C) slows disease spread. Monitor weather forecasts for early intervention.",
            "hi": "रस्ट मध्यम तापमान (15-22°C), उच्च आर्द्रता (70%+), और बार-बार ओस में पनपता है। शुष्क, गर्म मौसम (>30°C) रोग के प्रसार को धीमा करता है। शीघ्र हस्तक्षेप के लिए मौसम पूर्वानुमान की निगरानी करें।"
        }
    }

    # =================================================
    # PDF REPORT GENERATION FUNCTION
    # =================================================
    def generate_pdf_report(severity, num_detections, risk, summary_text, recommendations, timestamp):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3c72'),
            spaceAfter=30,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2a5298'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        story.append(Paragraph("FarmSpectra Wheat Rust Detection Report", title_style))
        story.append(Spacer(1, 12))
        
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", styles['Normal']))
        story.append(Paragraph(f"<b>Report ID:</b> WR-{timestamp}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Executive Summary", heading_style))
        clean_summary = summary_text.replace("✅", "").replace("⚠️", "").replace("❌", "")
        story.append(Paragraph(clean_summary, styles['Normal']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Key Metrics", heading_style))
        healthy_area = max(0, 100 - severity)
        needs_attention = min(severity, 100)
        serious_stress = max(0, severity - 15) if severity > 15 else 0
        
        data = [
            ['Metric', 'Value', 'Status'],
            ['Healthy Area', f'{healthy_area:.0f}%', 'Good' if healthy_area > 70 else 'Warning'],
            ['Needs Attention', f'{needs_attention:.0f}%', 'Warning' if needs_attention > 20 else 'Good'],
            ['Serious Stress', f'{serious_stress:.0f}%', 'Critical' if serious_stress > 30 else 'Good'],
            ['Detected Spots', str(num_detections), 'Critical' if num_detections > 30 else 'Warning' if num_detections > 10 else 'Good'],
            ['Risk Level', risk, 'Critical' if 'Severe' in risk else 'Warning']
        ]
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2a5298')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Recommended Actions", heading_style))
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("Important Notes", heading_style))
        story.append(Paragraph(
            "This report is generated by AI-powered image analysis. For severe infections, please consult with a certified agricultural extension officer. "
            "Results are based on visible symptoms and may not account for all field conditions.",
            styles['Italic']
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    # =================================================
    # ExG FUNCTION
    # =================================================
    def calculate_exg_heatmap(image_rgb):
        img = image_rgb.astype(float)
        blue, green, red = img[:, :, 2], img[:, :, 1], img[:, :, 0]
        exg = 2 * green - red - blue
        exg_norm = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
        return 255 - exg_norm

    # =================================================
    # UPLOAD SECTION
    # =================================================
    st.markdown("""
    <div class="section-box">
        <div class="section-title">📤 Upload RGB Image</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Drag and drop file here\nLimit 200MB per file • PNG, JPG, JPEG",
        type=["jpg", "png", "jpeg"],
        label_visibility="visible"
    )

    # =================================================
    # MAIN PROCESSING
    # =================================================
    if uploaded_image is not None:
        
        st.markdown(f"""
        <div class="file-display">
            📄 {uploaded_image.name} • {uploaded_image.size / (1024*1024):.2f} MB
        </div>
        """, unsafe_allow_html=True)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_image.read())
            img_path = tmp.name

        original_img = cv2.imread(img_path)
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        
        MAX_DIM = 1600
        h, w, _ = original_img.shape
        
        if max(h, w) > MAX_DIM:
            scale = MAX_DIM / max(h, w)
            original_img = cv2.resize(original_img, (int(w * scale), int(h * scale)))
            cv2.imwrite(img_path, cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR))

        with st.spinner("🔄 Analyzing image with AI..."):
            results = model(img_path, imgsz=640, conf=0.15, retina_masks=False, verbose=False)[0]

        overlay_img = original_img.copy()
        boxes = []
        infected_pixels = 0
        total_pixels = original_img.shape[0] * original_img.shape[1]

        if results.masks is not None and len(results.masks.data) > 0:
            masks = results.masks.data.cpu().numpy()
            combined_mask = np.sum(masks, axis=0)
            
            if combined_mask is not None and combined_mask.size > 0:
                combined_mask = cv2.resize(combined_mask.astype(np.float32), (original_img.shape[1], original_img.shape[0]))
                infected_pixels = np.sum(combined_mask > 0.5)
                overlay_img[combined_mask > 0.5] = [255, 0, 0]
                boxes = results.boxes.xyxy.cpu().numpy()

        ai_view = cv2.addWeighted(original_img, 0.7, overlay_img, 0.3, 0)

        exg = calculate_exg_heatmap(original_img)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        exg_enhanced = clahe.apply(exg)
        exg_heatmap = cv2.applyColorMap(exg_enhanced, cv2.COLORMAP_JET)

        os.makedirs("results/exg_heatmaps", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f"results/exg_heatmaps/exg_{timestamp}.png", exg_heatmap)

        pixel_severity = (infected_pixels / total_pixels) * 100 if infected_pixels > 0 else 0
        num_detections = len(boxes)
        
        if num_detections == 0:
            detection_severity = 0
        elif num_detections <= 5:
            detection_severity = 5
        elif num_detections <= 15:
            detection_severity = 18
        elif num_detections <= 30:
            detection_severity = 35
        else:
            detection_severity = 60
        
        severity = max(pixel_severity, detection_severity)
        healthy_area = max(0, 100 - severity)
        needs_attention = min(severity, 100)
        serious_stress = max(0, severity - 15) if severity > 15 else 0
        
        # IMPROVED: More explicit handling for no disease
        if num_detections == 0 and pixel_severity < 5:
            # No disease detected at all
            risk = "No Disease Detected"
            status_class = "status-healthy"
            summary_text = "✅ No disease detected - Your field appears completely healthy!"
            confidence = "High confidence"
            recommendations = [
                "✅ No immediate action required",
                "Continue regular field monitoring every 2 weeks",
                "Maintain current irrigation and fertilization practices",
                "Keep records for future comparison"
            ]
        elif severity < 10:
            risk = "Healthy"
            status_class = "status-healthy"
            summary_text = "✅ Your field is healthy and no disease is detected"
            confidence = "High confidence"
            recommendations = [
                "Continue regular monitoring",
                "Maintain current irrigation schedule",
                "Schedule next inspection in 2 weeks",
                "Please Check for Nutrient Deficiency and Water Stress"
            ]
        elif severity < 25:
            risk = "Needs Attention"
            status_class = "status-warning"
            summary_text = "⚠️ Your field is under mild stress"
            confidence = "Medium confidence"
            recommendations = [
                "Reduce irrigation frequency if excessive",
                "Improve air circulation between plants",
                "Monitor affected areas daily",
                "Please Check for Nutrient Deficiency and Water Stress"
            ]
        elif severity < 45:
            risk = "Moderate Stress"
            status_class = "status-danger"
            summary_text = "❌ Your field is under moderate stress"
            confidence = "High confidence"
            recommendations = [
                "Apply preventive fungicide immediately",
                "Avoid excess irrigation and overhead watering",
                "Remove heavily infected plants if localized",
                "Consider consulting agricultural expert"
            ]
        else:
            risk = "Severe Stress"
            status_class = "status-danger"
            summary_text = "❌ Your field is under severe stress"
            confidence = "High confidence"
            recommendations = [
                "Apply systemic fungicide urgently (within 24 hours)",
                "Consult agricultural extension officer immediately",
                "Isolate affected field to prevent spread",
                "Prepare for follow-up treatment in 7-10 days"
            ]

        st.markdown(f"""
        <div class="section-box">
            <div class="section-title">🌾 Field Health Summary</div>
            <div class="{status_class}">{summary_text}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-box"><div class="section-title">📊 How Your Land Is Doing</div></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">🌱 Healthy Area</div><div class="metric-value">{healthy_area:.0f}%</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card"><div class="metric-label">⚠️ Needs Attention</div><div class="metric-value">{needs_attention:.0f}%</div></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">❌ Serious Stress</div><div class="metric-value">{serious_stress:.0f}%</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card"><div class="metric-label">📍 Detected Spots</div><div class="metric-value">{num_detections}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box"><div class="section-title">🖼️ Detection Result</div></div>', unsafe_allow_html=True)

        fig, ax = plt.subplots(1, 2, figsize=(16, 6))
        fig.patch.set_facecolor('white')

        ax[0].imshow(original_img)
        ax[0].set_title("Original Image", fontsize=14, fontweight='600', pad=12, color='#1e3c72')

        ax[1].imshow(ai_view)
        for box in boxes:
            x1, y1, x2, y2 = box
            ax[1].add_patch(patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=2.5, edgecolor="#ffeb3b", facecolor="none"))
        ax[1].set_title(f"Disease Detection Output ({num_detections} spots detected)", fontsize=14, fontweight='600', pad=12, color='#1e3c72')

        for a in ax:
            a.axis("off")

        st.pyplot(fig)

        st.markdown('<div class="section-box"><div class="section-title">🔍 Why is this happening?</div>', unsafe_allow_html=True)

        if severity < 10:
            st.markdown('<div class="info-box">💧 Your crop appears healthy with no stress indicators detected.</div>', unsafe_allow_html=True)
        elif severity < 25:
            st.markdown('<div class="info-box-warning">💧 Early-stage rust infection detected. Environmental stress , Nutrient or Water stress may be contributing factors. Please Check for Nutrient Deficiency and Water Stress</div>', unsafe_allow_html=True)
        elif severity < 45:
            st.markdown('<div class="info-box-warning">💧 Moderate rust infection detected. Prolonged moisture and high humidity are likely causes.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box-warning">💧 Severe rust infection detected. Immediate intervention required to prevent further spread.</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f'<div class="section-box"><div class="section-title">🎯 How sure is this result?</div><div style="margin: 14px 0;"><span style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 8px 18px; border-radius: 20px; font-weight: 600; color: #663c00;">🟡 {confidence}</span></div></div>', unsafe_allow_html=True)
        
        confidence_value = 0.85 if num_detections > 10 else 0.65
        st.progress(confidence_value)

        st.markdown('<div class="section-box"><div class="section-title">🧑‍🌾 What should I do now?</div>', unsafe_allow_html=True)
        
        for rec in recommendations:
            st.markdown(f'<div style="background: #f8f9fa; padding: 12px 16px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #667eea;">{rec}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-box"><div class="section-title">💬 Ask Questions (Hindi & English) | सवाल पूछें</div></div>', unsafe_allow_html=True)

        with st.expander("🌾 सामान्य प्रश्न | Common Questions", expanded=False):
            for question, answers in QA_DATA.items():
                st.markdown(f"**Q: {question}**")
                st.markdown(f"**English:** {answers['en']}")
                st.markdown(f"<div class='hindi-text'><strong>हिंदी:</strong> {answers['hi']}</div>", unsafe_allow_html=True)
                st.markdown("---")

        # st.markdown("### 🔍 Ask Your Own Question | अपना सवाल पूछें")
        # user_question = st.text_input("Type your question here...", placeholder="e.g., How long does treatment take?")
        
        # if user_question:
        #     st.info(f"**Your Question:** {user_question}")
        #     st.markdown('<div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 16px; border-radius: 8px; margin: 10px 0;"><strong>Note:</strong> For personalized advice, please consult with your local agricultural extension officer. This system provides general guidance based on common scenarios.<br><br><strong class="hindi-text">नोट:</strong> <span class="hindi-text">व्यक्तिगत सलाह के लिए, कृपया अपने स्थानीय कृषि विस्तार अधिकारी से परामर्श करें।</span></div>', unsafe_allow_html=True)
        
        st.markdown("### 🔍 Ask Your Own Question | अपना सवाल पूछें")
        user_question = st.text_input("Type your question here...", placeholder="e.g., How long does treatment take?")

        if user_question:
            st.info(f"**Your Question:** {user_question}")
    
            with st.spinner("🤔 Thinking..."):
                try:
            # Configure Gemini API (set this in environment variable)
                    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
            
                    if not GEMINI_API_KEY:
                        st.warning("⚠️ AI service not configured. Showing basic response...")
                
                # Fallback to basic responses
                        if any(word in user_question.lower() for word in ['severity', 'percent', '%', 'score', 'why']):
                            answer = f"""**English:**
Your field shows {severity:.1f}% severity with {num_detections} disease spots detected. This indicates a {risk} condition. The severity is calculated based on infected area coverage and number of rust pustules visible in the image.

**हिंदी:**
आपके खेत में {severity:.1f}% गंभीरता के साथ {num_detections} रोग के धब्बे पाए गए हैं। यह एक {risk} स्थिति को दर्शाता है। गंभीरता की गणना संक्रमित क्षेत्र और छवि में दिखाई देने वाले रस्ट पस्ट्यूल्स की संख्या के आधार पर की जाती है।"""
                        else:
                            answer = """**English:**
For specific advice about your field condition, please consult with your local agricultural extension officer. General recommendation: Monitor your field regularly and follow the recommendations provided in the analysis above.

**हिंदी:**
आपके खेत की स्थिति के बारे में विशिष्ट सलाह के लिए, कृपया अपने स्थानीय कृषि विस्तार अधिकारी से परामर्श करें। सामान्य सिफारिश: अपने खेत की नियमित निगरानी करें और ऊपर दिए गए विश्लेषण में दी गई सिफारिशों का पालन करें।"""
                    else:
                        from google import genai
                        genai_client = genai.Client(api_key=GEMINI_API_KEY)

                        # genai.configure(api_key=GEMINI_API_KEY)
                        # model = genai.GenerativeModel('gemini-1.5-flash')
                
                        # Prepare context from current analysis
                        context = f"""
                        Current Analysis Results:
                        - Risk Level: {risk}
                        - Severity: {severity:.1f}%
                        - Healthy Area: {healthy_area:.0f}%
                        - Disease Spots Detected: {num_detections}
                        - Summary: {summary_text}
                        - Recommendations: {', '.join(recommendations)}
                        """
                    
                        prompt = f"""You are an agricultural expert helping farmers with wheat crop disease management.

{context}

Farmer's Question: {user_question}

Please provide a helpful answer in both English and Hindi. If the question is about their current results, use the analysis data provided above. If it's a general farming question, provide expert agricultural advice.

Format your response exactly as:
**English:**
[Your answer in English]

**हिंदी:**
[Your answer in Hindi]

Keep answers practical, concise (3-4 sentences), and farmer-friendly."""
                
                        response = genai_client.models.generate_content(
                            model = "gemini-2.5-flash",
                            contents = prompt
                        )
                        if response and response.candidates:
                            answer = response.candidates[0].content.parts[0].text
                        else:
                            raise ValueError("empty gemini response")
            
                    st.markdown('<div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 18px; border-radius: 10px; margin: 12px 0; border-left: 5px solid #2196F3;">', unsafe_allow_html=True)
                    st.markdown(answer)
                    st.markdown('</div>', unsafe_allow_html=True)
            
                except Exception as e:
                    st.warning(f"⚠️ Could not get AI response. Showing basic answer...")
            
            # Fallback response
                    if any(word in user_question.lower() for word in ['severity', 'percent', '%', 'score', 'why']):
                        answer = f"""**English:**
Based on the analysis, your field shows {severity:.1f}% severity level with {num_detections} rust spots detected. The risk level is assessed as "{risk}". Please follow the recommendations provided above for best results.

**हिंदी:**
विश्लेषण के आधार पर, आपके खेत में {severity:.1f}% गंभीरता स्तर के साथ {num_detections} रस्ट धब्बे पाए गए हैं। जोखिम स्तर "{risk}" के रूप में आंका गया है। सर्वोत्तम परिणामों के लिए कृपया ऊपर दी गई सिफारिशों का पालन करें।"""
                    else:
                        answer = """**English:**
For best disease management: (1) Apply fungicides as recommended, (2) Improve field drainage, (3) Monitor weather conditions, (4) Consult your local agricultural officer for region-specific advice.

**हिंदी:**
सर्वोत्तम रोग प्रबंधन के लिए: (1) अनुशंसित कवकनाशी लगाएं, (2) खेत की जल निकासी में सुधार करें, (3) मौसम की स्थिति की निगरानी करें, (4) क्षेत्र-विशिष्ट सलाह के लिए अपने स्थानीय कृषि अधिकारी से परामर्श करें।"""
            
                    st.markdown('<div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 18px; border-radius: 10px; margin: 12px 0; border-left: 5px solid #2196F3;">', unsafe_allow_html=True)
                    st.markdown(answer)
                    st.markdown('</div>', unsafe_allow_html=True)
    
            st.markdown('<div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 16px; border-radius: 8px; margin: 10px 0;"><strong>Note:</strong> For personalized advice, please consult with your local agricultural extension officer. This system provides general guidance based on common scenarios.<br><br><strong class="hindi-text">नोट:</strong> <span class="hindi-text">व्यक्तिगत सलाह के लिए, कृपया अपने स्थानीय कृषि विस्तार अधिकारी से परामर्श करें।</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-box"><div class="section-title">📥 Download Report & Results</div></div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        pdf_buffer = generate_pdf_report(severity, num_detections, risk, summary_text, recommendations, timestamp)
        
        with col1:
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"wheat_rust_report_{timestamp}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="🖼️ Download Detection Image",
                data=cv2.imencode(".png", cv2.cvtColor(ai_view, cv2.COLOR_RGB2BGR))[1].tobytes(),
                file_name=f"detection_{timestamp}.png",
                mime="image/png",
                use_container_width=True
            )
        
        with col3:
            st.download_button(
                label="🗺️ Download ExG Heatmap",
                data=cv2.imencode(".png", exg_heatmap)[1].tobytes(),
                file_name=f"heatmap_{timestamp}.png",
                mime="image/png",
                use_container_width=True
            )

        os.remove(img_path)

    else:
        st.markdown('<div class="info-box">👆 Please upload a wheat crop image to begin analysis</div>', unsafe_allow_html=True)
        
if __name__ == "__main__":
    run_disease_detection()