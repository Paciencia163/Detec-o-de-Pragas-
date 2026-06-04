
import streamlit as st
from components import image_detection, video_detection, webcam_detection

def show_detection_hub(model_yolo):
    st.markdown("""
    <style>
    .detection-title {
        font-size: 48px;
        text-align: center;
        background: linear-gradient(135deg, #1e5631 0%, #40916c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        margin-bottom: 30px;
        animation: fadeIn 0.8s ease;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    [role="radiogroup"] {
        display: flex !important;
        gap: 15px !important;
        margin: 30px 0 !important;
        flex-wrap: wrap;
    }

    [role="radiogroup"] > label {
        flex: 1 !important;
        min-width: 200px !important;
        padding: 18px 25px !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        text-align: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 600 !important;
        color: #374151 !important;
        background: white !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }

    [role="radiogroup"] > label:hover {
        border-color: #40916c !important;
        background: #f0f9f7 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px rgba(64, 145, 108, 0.15) !important;
    }

    [role="radiogroup"] > label[data-selected="true"] {
        background: linear-gradient(135deg, #40916c 0%, #52b788 100%) !important;
        color: white !important;
        border-color: #40916c !important;
        box-shadow: 0 8px 20px rgba(64, 145, 108, 0.3) !important;
    }

    hr {
        border: none !important;
        border-top: 2px solid #e5e7eb !important;
        margin: 30px 0 !important;
    }

    .detection-content {
        animation: slideInUp 0.8s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='detection-title'>🔍 Hub de Detecção Inteligente</div>", unsafe_allow_html=True)

    detection_type = st.radio(
        "Selecione o Modo de Detecção:",
        ["📷 Detecção de Imagem", "🎥 Detecção de Vídeo", "📹 Webcam em Tempo Real"],
        horizontal=True
    )

    st.markdown("---")

    st.markdown("<div class='detection-content'>", unsafe_allow_html=True)

    if detection_type == "📷 Detecção de Imagem":
        image_detection.show(model_yolo)
    elif detection_type == "🎥 Detecção de Vídeo":
        video_detection.show(model_yolo)
    elif detection_type == "📹 Webcam em Tempo Real":
        webcam_detection.show(model_yolo)

    st.markdown("</div>", unsafe_allow_html=True)
