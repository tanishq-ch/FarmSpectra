import streamlit as st

st.set_page_config(
    page_title="FarmSpectra",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🌾 FarmSpectra")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate:",
    ["🏠 Home", "🔬 Disease Detection", "🌿 Weed Detection"]
)

st.sidebar.markdown("---")
st.sidebar.info("Select a feature from above")

if page == "🏠 Home":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                color: white; padding: 40px; border-radius: 15px; text-align: center;">
        <h1>🌾 FarmSpectra</h1>
        <p style="font-size: 20px;">Advanced Agricultural Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 12px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h2>🔬 Disease Detection</h2>
            <p style="font-size: 16px; line-height: 1.8;">
                • AI-powered wheat rust detection<br>
                • Detailed health analysis<br>
                • Severity assessment<br>
                • Treatment recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 12px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h2>🌿 Weed Detection</h2>
            <p style="font-size: 16px; line-height: 1.8;">
                • YOLO-based weed identification<br>
                • Real-time detection<br>
                • Severity classification<br>
                • Actionable insights
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.success("👈 **Select a feature from the sidebar!**")

elif page == "🔬 Disease Detection":
    from app import run_disease_detection
    run_disease_detection()

elif page == "🌿 Weed Detection":
    from Wheat_Weed_app import run_weed_detection
    run_weed_detection()