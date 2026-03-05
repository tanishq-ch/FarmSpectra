import numpy as np
import cv2
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from gtts import gTTS


# =====================================================
# NDVI CALCULATION
# =====================================================
def calculate_ndvi(rgb, nir):
    # Extract RED channel
    red = rgb[:, :, 2].astype(float)

    # Resize NIR to match RGB dimensions
    if nir.shape != red.shape:
        nir = cv2.resize(nir, (red.shape[1], red.shape[0]))

    nir = nir.astype(float)

    ndvi = (nir - red) / (nir + red + 1e-6)
    return np.clip(ndvi, -1, 1)


# =====================================================
# NDVI STRESS MAP & HEATMAP
# =====================================================
def ndvi_stress_map(ndvi):
    stress_map = np.zeros_like(ndvi, dtype=np.uint8)

    stress_map[ndvi < 0.1] = 0                 # Barren
    stress_map[(ndvi >= 0.1) & (ndvi < 0.3)] = 1  # Severe
    stress_map[(ndvi >= 0.3) & (ndvi < 0.5)] = 2  # Moderate
    stress_map[ndvi >= 0.5] = 3                # Healthy

    cmap = plt.cm.get_cmap("RdYlGn", 4)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(stress_map, cmap=cmap)
    ax.set_title("NDVI Stress Heatmap")
    ax.axis("off")

    return fig, stress_map


# =====================================================
# FIELD LEVEL CLASSIFICATION
# =====================================================
def classify_stress(ndvi_mean):
    return "Stressed" if ndvi_mean < 0.4 else "Healthy"


# =====================================================
# DROUGHT & NUTRIENT SCORING
# =====================================================
def drought_score(ndvi):
    return np.sum(ndvi < 0.3) / ndvi.size


def nutrient_score(ndvi):
    return np.sum((ndvi >= 0.3) & (ndvi < 0.5)) / ndvi.size


# =====================================================
# NORMALIZATION & CONFIDENCE
# =====================================================
def normalize(value, min_val=0, max_val=1):
    value = max(min(value, max_val), min_val)
    return (value - min_val) / (max_val - min_val + 1e-6)


def confidence_percentage(val1, val2):
    diff = abs(val1 - val2)
    return int(min(diff * 100, 100))


# =====================================================
# PDF REPORT GENERATION
# =====================================================
def generate_farmer_report(
    filename,
    status,
    issue,
    healthy,
    moderate,
    severe,
    barren
):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>FarmSpectra Crop Health Report</b>", styles["Title"]))
    content.append(Paragraph(f"Overall Status: <b>{status}</b>", styles["Normal"]))
    content.append(Paragraph(f"Main Issue Detected: <b>{issue}</b>", styles["Normal"]))
    content.append(Paragraph("<br/>Land Health Distribution:", styles["Normal"]))
    content.append(Paragraph(f"Healthy Area: {healthy:.1f}%", styles["Normal"]))
    content.append(Paragraph(f"Moderate Stress: {moderate:.1f}%", styles["Normal"]))
    content.append(Paragraph(f"Severe Stress: {severe:.1f}%", styles["Normal"]))
    content.append(Paragraph(f"Barren Area: {barren:.1f}%", styles["Normal"]))

    doc.build(content)


# =====================================================
# HINDI VOICE SUMMARY
# =====================================================
def generate_hindi_voice(
    filename,
    status,
    issue,
    healthy,
    moderate,
    severe,
    barren
):
    text = f"""
    आपकी फसल की स्थिति {status} है।
    मुख्य समस्या {issue} पाई गई है।
    स्वस्थ क्षेत्र {int(healthy)} प्रतिशत है।
    मध्यम तनाव {int(moderate)} प्रतिशत है।
    गंभीर तनाव {int(severe)} प्रतिशत है।
    बंजर क्षेत्र {int(barren)} प्रतिशत है।
    """

    tts = gTTS(text=text, lang="hi")
    tts.save(filename)
