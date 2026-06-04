import streamlit as st
import cv2
import pandas as pd
import numpy as np

@st.cache_data
def load_pest_info():
    try:
        return pd.read_csv(r"utils\detailed_pests_solutions.csv")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

def show(model):
    st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .webcam-title {
        font-size: 48px;
        text-align: center;
        background: linear-gradient(135deg, #1e5631 0%, #40916c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        margin-bottom: 10px;
        animation: fadeIn 0.8s ease;
    }

    .webcam-subtitle {
        text-align: center;
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 30px;
        animation: fadeIn 1s ease;
    }

    .webcam-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        background: #000;
        margin: 20px 0;
    }

    .control-section {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.8s ease;
    }

    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    .status-active {
        background-color: #4caf50;
    }

    .status-inactive {
        background-color: #9e9e9e;
    }

    .checkbox-label {
        font-size: 16px;
        font-weight: 600;
        color: #1e5631;
    }

    .pest-results {
        background: white;
        border-radius: 16px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.8s ease;
    }

    .pest-results h2 {
        color: #1e5631;
        font-weight: 700;
        font-size: 28px;
        margin-top: 0;
        padding-bottom: 15px;
        border-bottom: 2px solid #e5e7eb;
    }

    .pest-item {
        background: linear-gradient(135deg, rgba(64, 145, 108, 0.1) 0%, rgba(82, 183, 136, 0.05) 100%);
        border-left: 5px solid #40916c;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }

    .pest-item:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 20px rgba(64, 145, 108, 0.15);
    }

    .pest-item h3 {
        color: #1e5631;
        margin-top: 0;
        font-weight: 700;
        font-size: 22px;
    }

    .info-row {
        margin: 12px 0;
        padding: 8px 0;
        border-bottom: 1px solid rgba(64, 145, 108, 0.1);
    }

    .info-row:last-child {
        border-bottom: none;
    }

    .info-row strong {
        color: #1e5631;
        display: block;
        margin-bottom: 5px;
    }

    .info-row em {
        color: #6b7280;
    }

    .message-box {
        border-radius: 12px;
        padding: 16px;
        margin: 15px 0;
        font-weight: 600;
        animation: fadeIn 0.6s ease;
    }

    .message-warning {
        background: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
        color: #f57f17;
    }

    .message-success {
        background: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4caf50;
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='webcam-title'>📹 Detecção em Tempo Real</div>", unsafe_allow_html=True)
    st.markdown("<div class='webcam-subtitle'>Use sua webcam para detectar pragas em tempo real</div>", unsafe_allow_html=True)

    # Initialize session state
    if 'detected_pests' not in st.session_state:
        st.session_state.detected_pests = {}

    st.markdown("<div class='control-section'>", unsafe_allow_html=True)
    run = st.checkbox("▶️ Iniciar Webcam", label_visibility="visible")
    st.markdown("</div>", unsafe_allow_html=True)

    if run:
        pest_info_df = load_pest_info()
        if pest_info_df.empty:
            st.markdown("<div class='message-box message-warning'>⚠️ Arquivo de informações sobre pragas ausente ou vazio.</div>", unsafe_allow_html=True)
            return

        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        st.markdown("<div class='message-box message-success'><span class='status-indicator status-active'></span>✅ Transmitindo da webcam...</div>", unsafe_allow_html=True)

        frame_count = 0
        frame_skip = 3  # Process every 3 frames

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Webcam não detectada ou não disponível.")
                break

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue

            frame = cv2.resize(frame, (640, 640))

            results = model(frame)
            annotated = results[0].plot()

            with stframe.container():
                st.markdown("<div class='webcam-container'>", unsafe_allow_html=True)
                st.image(annotated, channels="BGR", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            names = results[0].names
            probs = results[0].probs

            if probs is not None and len(probs) > 0:
                probs_data = probs.data.cpu().numpy()
                for i in range(len(probs_data)):
                    score = float(probs_data[i])
                    name = names[i].lower()
                    if score > 0.70:
                        if name not in st.session_state.detected_pests or score > st.session_state.detected_pests[name]:
                            st.session_state.detected_pests[name] = score

        cap.release()
        stframe.empty()
        st.markdown("<div class='message-box message-success'><span class='status-indicator status-inactive'></span>✅ Webcam parada.</div>", unsafe_allow_html=True)

    # After unchecking "Start Webcam", display pest info
    if not run and st.session_state.detected_pests:
        st.markdown("<div class='pest-results'><h2>🐛 Pragas Detectadas</h2>", unsafe_allow_html=True)
        pest_info_df = load_pest_info()

        for pest, score in st.session_state.detected_pests.items():
            row = pest_info_df[pest_info_df["Pest Name"].str.lower() == pest]
            st.markdown(f"""
            <div class='pest-item'>
                <h3>🐛 {pest.title()} - {score * 100:.1f}% de Confiança</h3>
            """, unsafe_allow_html=True)
            if not row.empty:
                st.markdown(f"<div class='info-row'><strong>🔬 Nome Científico:</strong> <em>{row.iloc[0]['Scientific Name']}</em></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-row'><strong>📖 Descrição:</strong> {row.iloc[0]['Description']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-row'><strong>🛠️ Estratégias de Manejo:</strong> {row.iloc[0]['Management Strategies']}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='info-row'><em>Nenhuma informação adicional encontrada no banco de dados.</em></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Optional: Clear the detected pests after showing
        # st.session_state.detected_pests = {}
