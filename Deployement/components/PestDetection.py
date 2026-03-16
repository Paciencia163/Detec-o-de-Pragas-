
import streamlit as st
from components import image_detection, video_detection, webcam_detection

def show_detection_hub(model_yolo):
    st.title("🔍 Hub de Detecção Inteligente")

    detection_type = st.radio(
        "Selecione o Modo de Detecção:",
        ["📷 Detecção de Imagem", "🎥 Detecção de Vídeo", "📹 Webcam em Tempo Real"],
        horizontal=True
    )

    st.markdown("---")

    if detection_type == "📷 Detecção de Imagem":
        image_detection.show(model_yolo)
    elif detection_type == "🎥 Detecção de Vídeo":
        video_detection.show(model_yolo)
    elif detection_type == "📹 Webcam em Tempo Real":
        webcam_detection.show(model_yolo)
