import streamlit as st
import cv2
from ultralytics import YOLO

from auth.login import login_screen
from components import home, image_detection, video_detection, webcam_detection , PestDetection , fertilizer_page
from model.yolo_model import load_model_yolo


# Login check
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
    st.stop()

# Load YOLO model

model_yolo = load_model_yolo()

# Sidebar
st.set_page_config(page_title="�️ Kulima", layout="wide")
# --- Custom Sidebar Styling ---
st.markdown("""
    <style>
    /* General sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1e5631 0%, #2d8659 100%);
        padding: 40px 20px;
        box-shadow: 8px 0 20px rgba(0, 0, 0, 0.15);
        border-right: 2px solid #40916c;
    }

    /* Sidebar logo */
    [data-testid="stSidebar"] img {
        display: block;
        margin: 0 auto 20px;
        border-radius: 50%;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar title */
    .sidebar-title {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 15px;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* Sidebar subtitle */
    .sidebar-subtitle {
        font-size: 14px;
        text-align: center;
        color: #d4f1d4;
        margin-bottom: 30px;
        font-weight: 500;
    }

    /* Radio buttons */
    div[role="radiogroup"] {
        margin-top: 20px;
    }

    div[role="radiogroup"] > label {
        font-size: 16px;
        padding: 14px 18px;
        margin: 8px 0;
        border-radius: 12px;
        color: #1e5631;
        background-color: rgba(255, 255, 255, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        display: block;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.3);
        font-weight: 500;
        color: #ffffff;
    }

    div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.25);
        transform: translateY(-3px);
        border-color: rgba(255, 255, 255, 0.5);
    }

    div[role="radiogroup"] > label[data-selected="true"] {
        background: linear-gradient(135deg, #40916c 0%, #52b788 100%);
        color: white;
        font-weight: 700;
        border: 2px solid #52b788;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #40916c 0%, #52b788 100%);
        color: white;
        font-size: 16px;
        font-weight: 600;
        padding: 14px 28px;
        border: none;
        border-radius: 10px;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #52b788 0%, #74c69d 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }

    /* Logout button styling */
    .stButton > button.logout {
        background: linear-gradient(135deg, #d62828 0%, #f77f00 100%);
        box-shadow: 0 4px 12px rgba(214, 40, 40, 0.3);
    }

    .stButton > button.logout:hover {
        background: linear-gradient(135deg, #f77f00 0%, #fcbf49 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(214, 40, 40, 0.4);
    }

    </style>
""", unsafe_allow_html=True)



st.sidebar.markdown("<h1 style='text-align: center; color: white; margin-bottom: 10px;'>🏔️ Kulima</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #d4f1d4; font-size: 14px; font-weight: 500;'>Detecção Inteligente de Pragas</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 20px 0;'>", unsafe_allow_html=True)

if st.sidebar.button("🚪 Sair"):
    st.session_state.logged_in = False
    st.rerun()



page = st.sidebar.radio(
    "📌 Navegar para:",
    ["🏡 Início", "🔍 Detecção", "🌾 Recomendação de Fertilizante"]
)

if page == "🏡 Início":
    home.show()

elif page == "🔍 Detecção":
    PestDetection.show_detection_hub(model_yolo)
elif page == "🌾 Recomendação de Fertilizante":
    fertilizer_page.show_fertilizer_page()
