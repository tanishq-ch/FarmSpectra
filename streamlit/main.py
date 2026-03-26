# import streamlit as st

# st.set_page_config(
#     page_title="FarmSpectra",
#     page_icon="🌾",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.sidebar.title("🌾 FarmSpectra")
# st.sidebar.markdown("---")

# page = st.sidebar.radio(
#     "Navigate:",
#     ["🏠 Home", "🔬 Disease Detection", "🌿 Weed Detection"]
# )

# st.sidebar.markdown("---")
# st.sidebar.info("Select a feature from above")

# if page == "🏠 Home":
#     st.markdown("""
#     <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
#                 color: white; padding: 40px; border-radius: 15px; text-align: center;">
#         <h1>🌾 FarmSpectra</h1>
#         <p style="font-size: 20px;">Advanced Agricultural Intelligence Platform</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("""
#         <div style="background: white; padding: 30px; border-radius: 12px; 
#                     box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
#             <h2>🔬 Disease Detection</h2>
#             <p style="font-size: 16px; line-height: 1.8;">
#                 • AI-powered wheat rust detection<br>
#                 • Detailed health analysis<br>
#                 • Severity assessment<br>
#                 • Treatment recommendations
#             </p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div style="background: white; padding: 30px; border-radius: 12px; 
#                     box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
#             <h2>🌿 Weed Detection</h2>
#             <p style="font-size: 16px; line-height: 1.8;">
#                 • YOLO-based weed identification<br>
#                 • Real-time detection<br>
#                 • Severity classification<br>
#                 • Actionable insights
#             </p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.success("👈 **Select a feature from the sidebar!**")

# elif page == "🔬 Disease Detection":
#     from app import run_disease_detection
#     run_disease_detection()

# elif page == "🌿 Weed Detection":
#     from Wheat_Weed_app import run_weed_detection
#     run_weed_detection()


# import streamlit as st

# st.set_page_config(
#     page_title="FarmSpectra",
#     page_icon="🌾",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.sidebar.title("🌾 FarmSpectra")
# st.sidebar.markdown("---")

# page = st.sidebar.radio(
#     "Navigate:",
#     ["🏠 Home", "🔬 Disease Detection", "🌿 Weed Detection", "🌱 Nutrient & Stress Detection"]
# )

# st.sidebar.markdown("---")
# st.sidebar.info("Select a feature from above")

# if page == "🏠 Home":
#     st.markdown("""
#     <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
#                 color: white; padding: 40px; border-radius: 15px; text-align: center;">
#         <h1>🌾 FarmSpectra</h1>
#         <p style="font-size: 20px;">Advanced Agricultural Intelligence Platform</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown("""
#         <div style="background: white; padding: 30px; border-radius: 12px; 
#                     box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
#             <h2>🔬 Disease Detection</h2>
#             <p style="font-size: 16px; line-height: 1.8;">
#                 • AI-powered wheat rust detection<br>
#                 • Detailed health analysis<br>
#                 • Severity assessment<br>
#                 • Treatment recommendations
#             </p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div style="background: white; padding: 30px; border-radius: 12px; 
#                     box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
#             <h2>🌿 Weed Detection</h2>
#             <p style="font-size: 16px; line-height: 1.8;">
#                 • YOLO-based weed identification<br>
#                 • Real-time detection<br>
#                 • Severity classification<br>
#                 • Actionable insights
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

#     with col3:
#         st.markdown("""
#         <div style="background: white; padding: 30px; border-radius: 12px; 
#                     box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
#             <h2>🌱 Nutrient & Stress Detection</h2>
#             <p style="font-size: 16px; line-height: 1.8;">
#                 • NDVI-based crop stress analysis<br>
#                 • Drought vs nutrient diagnosis<br>
#                 • Field health heatmaps<br>
#                 • Hindi voice summary & PDF report
#             </p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("<br>", unsafe_allow_html=True)
#     st.success("👈 **Select a feature from the sidebar!**")

# elif page == "🔬 Disease Detection":
#     from app import run_disease_detection
#     run_disease_detection()

# elif page == "🌿 Weed Detection":
#     from Wheat_Weed_app import run_weed_detection
#     run_weed_detection()

# elif page == "🌱 Nutrient & Stress Detection":
#     from Nutrient import run_nutrient_detection
#     run_nutrient_detection()


import streamlit as st

st.set_page_config(
    page_title="FarmSpectra",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1f0f !important;
    border-right: 1px solid #1e3d1f;
}
section[data-testid="stSidebar"] * {
    color: #c8e6c9 !important;
}

/* Hide radio label, style options as pill rows */
div[data-testid="stRadio"] > div {
    gap: 8px;
}
div[data-testid="stRadio"] label {
    background: #162918 !important;
    border: 1px solid #2e5430 !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
}
div[data-testid="stRadio"] label:hover {
    background: #1e3d20 !important;
    border-color: #4caf50 !important;
}

/* Main area */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 960px;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #071a08 0%, #0f2d11 50%, #0a2310 100%);
    border: 1px solid #1e4020;
    border-radius: 20px;
    padding: 52px 48px;
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(76,175,80,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #66bb6a;
    margin-bottom: 12px;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 48px;
    font-weight: 800;
    color: #f1f8e9;
    margin: 0 0 12px 0;
    line-height: 1.1;
}
.hero p {
    font-size: 17px;
    color: #a5d6a7;
    font-weight: 300;
    margin: 0;
    max-width: 520px;
    line-height: 1.7;
}

/* Section title */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #66bb6a;
    margin: 2rem 0 1rem 0;
}

/* Image type cards */
.img-card {
    background: #0a1f0b;
    border: 1.5px solid #1e3d20;
    border-radius: 16px;
    padding: 32px 28px;
    transition: all 0.25s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.img-card::after {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2e7d32, #66bb6a);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}
.img-card:hover {
    border-color: #4caf50;
    background: #0d2810;
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(76,175,80,0.15);
}
.img-card:hover::after { transform: scaleX(1); }
.img-card .icon {
    font-size: 42px;
    margin-bottom: 16px;
    display: block;
}
.img-card h3 {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #e8f5e9;
    margin: 0 0 10px 0;
}
.img-card p {
    font-size: 14px;
    color: #81c784;
    line-height: 1.7;
    margin: 0;
    font-weight: 300;
}
.img-card .tag {
    display: inline-block;
    background: #1b3a1c;
    border: 1px solid #2e5430;
    border-radius: 20px;
    font-size: 11px;
    color: #a5d6a7;
    padding: 3px 10px;
    margin-top: 16px;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* Feature cards (ground sub-options) */
.feat-card {
    background: #081508;
    border: 1.5px solid #1a3319;
    border-radius: 14px;
    padding: 26px 24px;
    transition: all 0.2s ease;
    height: 100%;
}
.feat-card:hover {
    border-color: #43a047;
    background: #0b1e0c;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(67,160,71,0.12);
}
.feat-card .icon { font-size: 32px; margin-bottom: 12px; display: block; }
.feat-card h4 {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #e8f5e9;
    margin: 0 0 8px 0;
}
.feat-card p {
    font-size: 13px;
    color: #81c784;
    line-height: 1.6;
    margin: 0;
    font-weight: 300;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e4020, transparent);
    margin: 2rem 0;
}

/* Streamlit button override */
.stButton > button {
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important;
    color: #e8f5e9 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2e7d32, #388e3c) !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(46,125,50,0.35) !important;
}

/* Step breadcrumb */
.breadcrumb {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #4a7a4c;
    margin-bottom: 1.5rem;
    font-weight: 500;
}
.breadcrumb .active { color: #a5d6a7; }
.breadcrumb .sep { color: #2e5430; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "image_type" not in st.session_state:
    st.session_state.image_type = None   # "ground" | "aerial"
if "ground_tool" not in st.session_state:
    st.session_state.ground_tool = None  # "disease" | "weed"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='padding: 8px 0 20px 0;'>
            <div style='font-family: Syne, sans-serif; font-size: 24px; font-weight: 800; color: #a5d6a7;'>
                🌾 FarmSpectra
            </div>
            <div style='font-size: 11px; color: #4caf50; letter-spacing: 2px; margin-top: 4px; text-transform: uppercase;'>
                Agricultural Intelligence
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1px;background:#1e3d20;margin-bottom:20px'></div>", unsafe_allow_html=True)

    nav = st.radio(
        "Navigation",
        ["🏠  Home", "📡  Start Analysis"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:1px;background:#1e3d20;margin:20px 0'></div>", unsafe_allow_html=True)

    # Dynamic status panel
    if st.session_state.image_type:
        label = "🛰️ Aerial Image" if st.session_state.image_type == "aerial" else "📷 Ground Image"
        tool_label = ""
        if st.session_state.ground_tool == "disease":
            tool_label = "<div style='font-size:12px;color:#81c784;margin-top:4px;'>→ Disease Detection</div>"
        elif st.session_state.ground_tool == "weed":
            tool_label = "<div style='font-size:12px;color:#81c784;margin-top:4px;'>→ Weed Detection</div>"
        elif st.session_state.image_type == "aerial":
            tool_label = "<div style='font-size:12px;color:#81c784;margin-top:4px;'>→ Nutrient &amp; Stress</div>"

        st.markdown(f"""
            <div style='background:#0d2810;border:1px solid #2e5430;border-radius:10px;padding:14px;margin-bottom:16px;'>
                <div style='font-size:10px;color:#66bb6a;letter-spacing:2px;font-weight:700;margin-bottom:6px;text-transform:uppercase;'>
                    Active Session
                </div>
                <div style='font-size:14px;color:#c8e6c9;font-weight:500;'>{label}</div>
                {tool_label}
            </div>
        """, unsafe_allow_html=True)

        if st.button("↩ Start Over", use_container_width=True):
            st.session_state.image_type = None
            st.session_state.ground_tool = None
            st.rerun()
    else:
        st.markdown("""
            <div style='font-size:13px;color:#4a7a4c;line-height:1.8;'>
                Upload field images to detect crop disease, weed infestation, or nutrient &amp; drought stress.
            </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if nav == "🏠  Home":
    st.session_state.image_type = None
    st.session_state.ground_tool = None

    st.markdown("""
        <div class="hero">
            <div class="hero-label">Precision Agriculture</div>
            <h1>FarmSpectra</h1>
            <p>AI-powered crop health analysis — from disease detection to nutrient stress mapping — built for farmers, backed by science.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">What You Can Detect</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="img-card">
                <span class="icon">🔬</span>
                <h3>Disease Detection</h3>
                <p>AI-powered identification of wheat rust and fungal infections with severity scoring.</p>
                <span class="tag">📷 Ground Image</span>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="img-card">
                <span class="icon">🌿</span>
                <h3>Weed Detection</h3>
                <p>YOLO-based real-time weed identification with field coverage and action thresholds.</p>
                <span class="tag">📷 Ground Image</span>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="img-card">
                <span class="icon">🛰️</span>
                <h3>Nutrient & Stress</h3>
                <p>NDVI-based aerial analysis diagnosing drought stress vs nutrient deficiency across your field.</p>
                <span class="tag">📡 Aerial / Drone Image</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align:center;color:#4a7a4c;font-size:14px;'>
            👈 Click <strong style='color:#66bb6a;'>Start Analysis</strong> in the sidebar to begin
        </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS FLOW
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📡  Start Analysis":

    # ── STEP 1: Choose image type ──────────────────────────────────────────────
    if st.session_state.image_type is None:

        st.markdown("""
            <div class="breadcrumb">
                <span class="active">Image Type</span>
                <span class="sep">›</span>
                <span>Tool</span>
                <span class="sep">›</span>
                <span>Analysis</span>
            </div>
            <div style='font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:#e8f5e9;margin-bottom:6px;'>
                What type of image do you have?
            </div>
            <div style='font-size:15px;color:#81c784;font-weight:300;margin-bottom:2.5rem;'>
                Choose based on how your photo was taken — this determines which analysis tools are available.
            </div>
        """, unsafe_allow_html=True)

        col1, spacer, col2 = st.columns([5, 1, 5])

        with col1:
            st.markdown("""
                <div class="img-card" style="padding:40px 32px;">
                    <span class="icon">📷</span>
                    <h3>Ground Image</h3>
                    <p>Photos taken from the ground or at crop level — standard smartphone or camera shots of your field.</p>
                    <span class="tag">Disease Detection &nbsp;·&nbsp; Weed Detection</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("I have a Ground Image →", key="btn_ground", use_container_width=True):
                st.session_state.image_type = "ground"
                st.rerun()

        with col2:
            st.markdown("""
                <div class="img-card" style="padding:40px 32px;">
                    <span class="icon">🛰️</span>
                    <h3>Aerial / Drone Image</h3>
                    <p>Top-down images captured by a drone or satellite. Requires an RGB + NIR image pair for NDVI analysis.</p>
                    <span class="tag">Nutrient &amp; Stress Detection</span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("I have an Aerial Image →", key="btn_aerial", use_container_width=True):
                st.session_state.image_type = "aerial"
                st.rerun()

    # ── STEP 2a: Ground — pick tool ────────────────────────────────────────────
    elif st.session_state.image_type == "ground" and st.session_state.ground_tool is None:

        st.markdown("""
            <div class="breadcrumb">
                <span>Image Type</span>
                <span class="sep">›</span>
                <span class="active">Tool</span>
                <span class="sep">›</span>
                <span>Analysis</span>
            </div>
            <div style='font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:#e8f5e9;margin-bottom:6px;'>
                What would you like to check?
            </div>
            <div style='font-size:15px;color:#81c784;font-weight:300;margin-bottom:2.5rem;'>
                You have a <strong style='color:#a5d6a7;'>Ground Image</strong>. Select the type of issue to analyse.
            </div>
        """, unsafe_allow_html=True)

        col1, spacer, col2 = st.columns([5, 1, 5])

        with col1:
            st.markdown("""
                <div class="feat-card">
                    <span class="icon">🔬</span>
                    <h4>Disease Detection</h4>
                    <p>Identify wheat rust, blight, and fungal infections. Get severity scores and treatment recommendations.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Check for Disease →", key="btn_disease", use_container_width=True):
                st.session_state.ground_tool = "disease"
                st.rerun()

        with col2:
            st.markdown("""
                <div class="feat-card">
                    <span class="icon">🌿</span>
                    <h4>Weed Detection</h4>
                    <p>YOLO-powered real-time weed identification with bounding boxes and infestation severity scoring.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Check for Weeds →", key="btn_weed", use_container_width=True):
                st.session_state.ground_tool = "weed"
                st.rerun()

    # ── STEP 2b: Aerial → Nutrient ─────────────────────────────────────────────
    elif st.session_state.image_type == "aerial":
        st.markdown("""
            <div class="breadcrumb">
                <span>Image Type</span>
                <span class="sep">›</span>
                <span class="active">Nutrient &amp; Stress Analysis</span>
            </div>
        """, unsafe_allow_html=True)
        from Nutrient import run_nutrient_detection
        run_nutrient_detection()

    # ── STEP 3a: Disease ───────────────────────────────────────────────────────
    elif st.session_state.image_type == "ground" and st.session_state.ground_tool == "disease":
        st.markdown("""
            <div class="breadcrumb">
                <span>Image Type</span>
                <span class="sep">›</span>
                <span>Tool</span>
                <span class="sep">›</span>
                <span class="active">Disease Detection</span>
            </div>
        """, unsafe_allow_html=True)
        from app import run_disease_detection
        run_disease_detection()

    # ── STEP 3b: Weed ──────────────────────────────────────────────────────────
    elif st.session_state.image_type == "ground" and st.session_state.ground_tool == "weed":
        st.markdown("""
            <div class="breadcrumb">
                <span>Image Type</span>
                <span class="sep">›</span>
                <span>Tool</span>
                <span class="sep">›</span>
                <span class="active">Weed Detection</span>
            </div>
        """, unsafe_allow_html=True)
        from Wheat_Weed_app import run_weed_detection
        run_weed_detection()