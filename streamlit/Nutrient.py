# import streamlit as st
# import cv2
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap
# from gtts import gTTS
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas


# # ---------------- NDVI FUNCTIONS ----------------

# def calculate_ndvi(rgb_img, nir_img):
#     red = rgb_img[:, :, 0].astype(float)

#     nir_resized = cv2.resize(
#         nir_img,
#         (red.shape[1], red.shape[0]),
#         interpolation=cv2.INTER_LINEAR
#     ).astype(float)

#     ndvi = (nir_resized - red) / (nir_resized + red + 1e-6)
#     return ndvi


# def ndvi_heatmap(ndvi):
#     fig, ax = plt.subplots()
#     im = ax.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
#     plt.colorbar(im, ax=ax, label="NDVI")
#     ax.set_title("NDVI Heatmap")
#     ax.axis("off")
#     return fig


# def ndvi_stress_map(ndvi):

#     stress_map = np.zeros_like(ndvi)

#     stress_map[ndvi < 0.1] = 0
#     stress_map[(ndvi >= 0.1) & (ndvi < 0.3)] = 1
#     stress_map[(ndvi >= 0.3) & (ndvi < 0.5)] = 2
#     stress_map[ndvi >= 0.5] = 3

#     cmap = ListedColormap([
#         "#8B0000",
#         "#FF4500",
#         "#FFD700",
#         "#228B22"
#     ])

#     labels = [
#         "Barren / No vegetation",
#         "Severely Stressed",
#         "Moderately Stressed",
#         "Healthy Vegetation"
#     ]

#     fig, ax = plt.subplots()
#     im = ax.imshow(stress_map, cmap=cmap)
#     ax.set_title("NDVI Stress Classification Map")
#     ax.axis("off")

#     cbar = plt.colorbar(im, ax=ax, ticks=[0.5, 1.5, 2.5, 3.5])
#     cbar.ax.set_yticklabels(labels)

#     return fig, stress_map


# # ---------------- NORMALIZE FUNCTIONS ----------------

# def normalize(value, min_val=0, max_val=1):
#     value = max(min(value, max_val), min_val)
#     return round((value - min_val) / (max_val - min_val + 1e-6), 3)


# def confidence_percentage(a, b):
#     diff = abs(a - b)
#     return round(min(diff * 100, 100), 2)


# # ---------------- REPORT GENERATION ----------------

# def generate_farmer_report(
#     filename,
#     field_status,
#     main_issue,
#     healthy_pct,
#     moderate_pct,
#     severe_pct,
#     barren_pct
# ):

#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4

#     c.setFont("Helvetica-Bold", 18)
#     c.drawString(50, height - 50, "FarmSpectra – Crop Health Report")

#     c.setFont("Helvetica", 12)
#     c.drawString(50, height - 100, f"Field Status: {field_status}")
#     c.drawString(50, height - 130, f"Main Issue Detected: {main_issue}")

#     c.drawString(50, height - 180, "Land Condition Summary:")
#     c.drawString(70, height - 210, f"Healthy Area: {healthy_pct:.0f}%")
#     c.drawString(70, height - 235, f"Needs Attention: {moderate_pct:.0f}%")
#     c.drawString(70, height - 260, f"Serious Stress: {severe_pct:.0f}%")
#     c.drawString(70, height - 285, f"No Crop Area: {barren_pct:.0f}%")

#     c.drawString(50, height - 340, "Recommended Action:")

#     if "Drought" in main_issue:
#         c.drawString(70, height - 370, "• Improve irrigation and watering frequency")
#     else:
#         c.drawString(70, height - 370, "• Apply recommended fertilizer after soil test")

#     c.save()


# # ---------------- VOICE GENERATION ----------------

# def generate_hindi_voice(
#     filename,
#     field_status,
#     main_issue,
#     healthy_pct,
#     moderate_pct,
#     severe_pct,
#     barren_pct
# ):

#     if field_status == "Stressed":
#         status_text = "आपका खेत तनाव में है।"
#     else:
#         status_text = "आपका खेत स्वस्थ है।"

#     issue_text = (
#         "मुख्य समस्या पानी की कमी है।"
#         if "Drought" in main_issue
#         else "मुख्य समस्या पोषक तत्वों की कमी है।"
#     )

#     summary_text = (
#         f"आपके खेत का विश्लेषण पूरा हो गया है। "
#         f"{status_text} "
#         f"{issue_text} "
#         f"लगभग {healthy_pct:.0f} प्रतिशत क्षेत्र स्वस्थ है। "
#         f"{moderate_pct:.0f} प्रतिशत क्षेत्र को ध्यान देने की आवश्यकता है। "
#         f"{severe_pct:.0f} प्रतिशत क्षेत्र गंभीर तनाव में है। "
#         f"{barren_pct:.0f} प्रतिशत क्षेत्र में फसल नहीं है। "
#     )

#     tts = gTTS(text=summary_text, lang="hi")
#     tts.save(filename)

#     return filename


# # ---------------- STRESS CLASSIFICATION ----------------

# def classify_stress(ndvi_mean):
#     if ndvi_mean < 0.4:
#         return "Stressed"
#     return "Healthy"


# # ---------------- DROUGHT / NUTRIENT ----------------

# def drought_score(ndvi):
#     return abs(ndvi.mean() - 0.2)


# def nutrient_score(ndvi):
#     return abs(ndvi.mean() - 0.5)


# # ---------------- STREAMLIT APP ----------------

# st.set_page_config(
#     page_title="FarmSpectra – Crop Stress Detection",
#     layout="centered"
# )

# st.title("🌱 FarmSpectra – Crop Stress Detection System")

# rgb_file = st.file_uploader("📷 Upload RGB Image", ["png", "jpg", "jpeg"])
# nir_file = st.file_uploader("📡 Upload NIR Image", ["png", "jpg", "jpeg"])


# if rgb_file and nir_file:

#     rgb = cv2.imdecode(
#         np.frombuffer(rgb_file.read(), np.uint8),
#         cv2.IMREAD_COLOR
#     )

#     nir = cv2.imdecode(
#         np.frombuffer(nir_file.read(), np.uint8),
#         cv2.IMREAD_GRAYSCALE
#     )

#     ndvi = calculate_ndvi(rgb, nir)
#     ndvi_mean = float(ndvi.mean())

#     status = classify_stress(ndvi_mean)
#     main_issue = "No Issue Detected"

#     st.markdown("## 🌾 Field Health Summary")

#     if status == "Stressed":
#         st.error("❌ Your field is under stress")
#     else:
#         st.success("✅ Your field is healthy")

#     st.markdown("## 🗺️ Field Health Map")

#     stress_fig, stress_map = ndvi_stress_map(ndvi)
#     st.pyplot(stress_fig)

#     total_pixels = stress_map.size

#     barren_pct = (stress_map == 0).sum() / total_pixels * 100
#     severe_pct = (stress_map == 1).sum() / total_pixels * 100
#     moderate_pct = (stress_map == 2).sum() / total_pixels * 100
#     healthy_pct = (stress_map == 3).sum() / total_pixels * 100

#     st.markdown("## 📊 How Your Land Is Doing")

#     col1, col2 = st.columns(2)

#     col1.metric("🌾 Healthy Area", f"{healthy_pct:.0f}%")
#     col1.metric("⚠️ Needs Attention", f"{moderate_pct:.0f}%")

#     col2.metric("❌ Serious Stress", f"{severe_pct:.0f}%")
#     col2.metric("🟤 No Crop Area", f"{barren_pct:.0f}%")

#     if status == "Stressed":

#         drought_val = normalize(drought_score(ndvi))
#         nutrient_val = normalize(nutrient_score(ndvi))

#         st.markdown("## 🔍 Why is this happening?")

#         if drought_val > nutrient_val:
#             main_issue = "Drought Stress (Water Shortage)"
#             st.info("💧 Water shortage is the main issue affecting your crops.")
#         else:
#             main_issue = "Nutrient Deficiency"
#             st.info("🧪 Lack of nutrients is affecting your crops.")

#         confidence = confidence_percentage(drought_val, nutrient_val)

#         st.markdown("## 🤝 How sure is this result?")

#         if confidence > 20:
#             st.success("🟢 High confidence")
#         else:
#             st.warning("🟡 Low confidence – try images from another date")

#         st.progress(confidence / 100)

#         with st.expander("🧑‍🌾 What should I do now?"):

#             if "Drought" in main_issue:
#                 st.markdown("""
#                 - 🚿 Improve irrigation coverage  
#                 - 🕒 Increase watering frequency  
#                 - 🌱 Avoid fertilizer until water stress reduces  
#                 """)
#             else:
#                 st.markdown("""
#                 - 🧪 Conduct soil testing  
#                 - 🌾 Apply recommended fertilizer  
#                 - 🚫 Avoid over-watering  
#                 """)

#         st.markdown("## 📄 Download Report")

#         if st.button("Download Farmer Report (PDF)"):

#             report_path = "FarmSpectra_Report.pdf"

#             generate_farmer_report(
#                 report_path,
#                 status,
#                 main_issue,
#                 healthy_pct,
#                 moderate_pct,
#                 severe_pct,
#                 barren_pct
#             )

#             with open(report_path, "rb") as f:
#                 st.download_button(
#                     "⬇️ Click here to download",
#                     f,
#                     file_name="FarmSpectra_Report.pdf"
#                 )

#     # ---------------- HINDI VOICE ----------------

#     st.markdown("## 🔊 हिंदी में सुनें (Listen in Hindi)")

#     if st.button("▶️ खेत की स्थिति सुनें"):

#         audio_file = "farm_voice_hindi.mp3"

#         generate_hindi_voice(
#             audio_file,
#             status,
#             main_issue,
#             healthy_pct,
#             moderate_pct,
#             severe_pct,
#             barren_pct
#         )

#         audio_bytes = open(audio_file, "rb").read()
#         st.audio(audio_bytes, format="audio/mp3")


import streamlit as st
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from gtts import gTTS
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ---------------- NDVI FUNCTIONS ----------------

def calculate_ndvi(rgb_img, nir_img):
    red = rgb_img[:, :, 0].astype(float)

    nir_resized = cv2.resize(
        nir_img,
        (red.shape[1], red.shape[0]),
        interpolation=cv2.INTER_LINEAR
    ).astype(float)

    ndvi = (nir_resized - red) / (nir_resized + red + 1e-6)
    return ndvi


def ndvi_heatmap(ndvi):
    fig, ax = plt.subplots()
    im = ax.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax, label="NDVI")
    ax.set_title("NDVI Heatmap")
    ax.axis("off")
    return fig


def ndvi_stress_map(ndvi):
    stress_map = np.zeros_like(ndvi)

    stress_map[ndvi < 0.1] = 0
    stress_map[(ndvi >= 0.1) & (ndvi < 0.3)] = 1
    stress_map[(ndvi >= 0.3) & (ndvi < 0.5)] = 2
    stress_map[ndvi >= 0.5] = 3

    cmap = ListedColormap([
        "#8B0000",
        "#FF4500",
        "#FFD700",
        "#228B22"
    ])

    labels = [
        "Barren / No vegetation",
        "Severely Stressed",
        "Moderately Stressed",
        "Healthy Vegetation"
    ]

    fig, ax = plt.subplots()
    im = ax.imshow(stress_map, cmap=cmap)
    ax.set_title("NDVI Stress Classification Map")
    ax.axis("off")

    cbar = plt.colorbar(im, ax=ax, ticks=[0.5, 1.5, 2.5, 3.5])
    cbar.ax.set_yticklabels(labels)

    return fig, stress_map


# ---------------- NORMALIZE FUNCTIONS ----------------

def normalize(value, min_val=0, max_val=1):
    value = max(min(value, max_val), min_val)
    return round((value - min_val) / (max_val - min_val + 1e-6), 3)


def confidence_percentage(a, b):
    diff = abs(a - b)
    return round(min(diff * 100, 100), 2)


# ---------------- REPORT GENERATION ----------------

def generate_farmer_report(
    filename,
    field_status,
    main_issue,
    healthy_pct,
    moderate_pct,
    severe_pct,
    barren_pct
):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "FarmSpectra – Crop Health Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Field Status: {field_status}")
    c.drawString(50, height - 130, f"Main Issue Detected: {main_issue}")

    c.drawString(50, height - 180, "Land Condition Summary:")
    c.drawString(70, height - 210, f"Healthy Area: {healthy_pct:.0f}%")
    c.drawString(70, height - 235, f"Needs Attention: {moderate_pct:.0f}%")
    c.drawString(70, height - 260, f"Serious Stress: {severe_pct:.0f}%")
    c.drawString(70, height - 285, f"No Crop Area: {barren_pct:.0f}%")

    c.drawString(50, height - 340, "Recommended Action:")

    if "Drought" in main_issue:
        c.drawString(70, height - 370, "• Improve irrigation and watering frequency")
    else:
        c.drawString(70, height - 370, "• Apply recommended fertilizer after soil test")

    c.save()


# ---------------- VOICE GENERATION ----------------

def generate_hindi_voice(
    filename,
    field_status,
    main_issue,
    healthy_pct,
    moderate_pct,
    severe_pct,
    barren_pct
):
    if field_status == "Stressed":
        status_text = "आपका खेत तनाव में है।"
    else:
        status_text = "आपका खेत स्वस्थ है।"

    issue_text = (
        "मुख्य समस्या पानी की कमी है।"
        if "Drought" in main_issue
        else "मुख्य समस्या पोषक तत्वों की कमी है।"
    )

    summary_text = (
        f"आपके खेत का विश्लेषण पूरा हो गया है। "
        f"{status_text} "
        f"{issue_text} "
        f"लगभग {healthy_pct:.0f} प्रतिशत क्षेत्र स्वस्थ है। "
        f"{moderate_pct:.0f} प्रतिशत क्षेत्र को ध्यान देने की आवश्यकता है। "
        f"{severe_pct:.0f} प्रतिशत क्षेत्र गंभीर तनाव में है। "
        f"{barren_pct:.0f} प्रतिशत क्षेत्र में फसल नहीं है। "
    )

    tts = gTTS(text=summary_text, lang="hi")
    tts.save(filename)

    return filename


# ---------------- STRESS CLASSIFICATION ----------------

def classify_stress(ndvi_mean):
    if ndvi_mean < 0.4:
        return "Stressed"
    return "Healthy"


# ---------------- DROUGHT / NUTRIENT ----------------

def drought_score(ndvi):
    return abs(ndvi.mean() - 0.2)


def nutrient_score(ndvi):
    return abs(ndvi.mean() - 0.5)


# ---------------- MAIN ENTRY POINT ----------------

def run_nutrient_detection():

    st.title("🌱 Crop Stress & Nutrient Detection")

    rgb_file = st.file_uploader("📷 Upload RGB Image", ["png", "jpg", "jpeg"])
    nir_file = st.file_uploader("📡 Upload NIR Image", ["png", "jpg", "jpeg"])

    if rgb_file and nir_file:

        rgb = cv2.imdecode(
            np.frombuffer(rgb_file.read(), np.uint8),
            cv2.IMREAD_COLOR
        )

        nir = cv2.imdecode(
            np.frombuffer(nir_file.read(), np.uint8),
            cv2.IMREAD_GRAYSCALE
        )

        ndvi = calculate_ndvi(rgb, nir)
        ndvi_mean = float(ndvi.mean())

        status = classify_stress(ndvi_mean)
        main_issue = "No Issue Detected"

        st.markdown("## 🌾 Field Health Summary")

        if status == "Stressed":
            st.error("❌ Your field is under stress")
        else:
            st.success("✅ Your field is healthy")

        st.markdown("## 🗺️ Field Health Map")

        stress_fig, stress_map = ndvi_stress_map(ndvi)
        st.pyplot(stress_fig)

        total_pixels = stress_map.size

        barren_pct = (stress_map == 0).sum() / total_pixels * 100
        severe_pct = (stress_map == 1).sum() / total_pixels * 100
        moderate_pct = (stress_map == 2).sum() / total_pixels * 100
        healthy_pct = (stress_map == 3).sum() / total_pixels * 100

        st.markdown("## 📊 How Your Land Is Doing")

        col1, col2 = st.columns(2)

        col1.metric("🌾 Healthy Area", f"{healthy_pct:.0f}%")
        col1.metric("⚠️ Needs Attention", f"{moderate_pct:.0f}%")

        col2.metric("❌ Serious Stress", f"{severe_pct:.0f}%")
        col2.metric("🟤 No Crop Area", f"{barren_pct:.0f}%")

        if status == "Stressed":

            drought_val = normalize(drought_score(ndvi))
            nutrient_val = normalize(nutrient_score(ndvi))

            st.markdown("## 🔍 Why is this happening?")

            if drought_val > nutrient_val:
                main_issue = "Drought Stress (Water Shortage)"
                st.info("💧 Water shortage is the main issue affecting your crops.")
            else:
                main_issue = "Nutrient Deficiency"
                st.info("🧪 Lack of nutrients is affecting your crops.")

            confidence = confidence_percentage(drought_val, nutrient_val)

            st.markdown("## 🤝 How sure is this result?")

            if confidence > 20:
                st.success("🟢 High confidence")
            else:
                st.warning("🟡 Low confidence – try images from another date")

            st.progress(confidence / 100)

            with st.expander("🧑‍🌾 What should I do now?"):

                if "Drought" in main_issue:
                    st.markdown("""
                    - 🚿 Improve irrigation coverage  
                    - 🕒 Increase watering frequency  
                    - 🌱 Avoid fertilizer until water stress reduces  
                    """)
                else:
                    st.markdown("""
                    - 🧪 Conduct soil testing  
                    - 🌾 Apply recommended fertilizer  
                    - 🚫 Avoid over-watering  
                    """)

            st.markdown("## 📄 Download Report")

            if st.button("Download Farmer Report (PDF)"):

                report_path = "FarmSpectra_Report.pdf"

                generate_farmer_report(
                    report_path,
                    status,
                    main_issue,
                    healthy_pct,
                    moderate_pct,
                    severe_pct,
                    barren_pct
                )

                with open(report_path, "rb") as f:
                    st.download_button(
                        "⬇️ Click here to download",
                        f,
                        file_name="FarmSpectra_Report.pdf"
                    )

        # ---------------- HINDI VOICE ----------------

        st.markdown("## 🔊 हिंदी में सुनें (Listen in Hindi)")

        if st.button("▶️ खेत की स्थिति सुनें"):

            audio_file = "farm_voice_hindi.mp3"

            generate_hindi_voice(
                audio_file,
                status,
                main_issue,
                healthy_pct,
                moderate_pct,
                severe_pct,
                barren_pct
            )

            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")