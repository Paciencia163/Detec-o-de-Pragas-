import streamlit as st
import cv2
import tempfile
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

    .video-title {
        font-size: 42px;
        text-align: center;
        color: #1e5631;
        font-weight: 700;
        margin-bottom: 10px;
        animation: fadeIn 0.8s ease;
    }

    .video-subtitle {
        text-align: center;
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 30px;
        animation: fadeIn 1s ease;
    }

    .video-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        margin: 30px 0;
        background: #000;
    }

    .pest-results {
        background: white;
        border-radius: 16px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
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

    .status-message {
        border-radius: 12px;
        padding: 16px;
        margin: 15px 0;
        font-weight: 600;
        animation: fadeIn 0.6s ease;
    }

    .status-info {
        background: rgba(13, 110, 253, 0.1);
        border-left: 4px solid #0d6efd;
        color: #0d5cb8;
    }

    .status-success {
        background: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4caf50;
        color: #2e7d32;
    }

    .status-warning {
        background: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
        color: #f57f17;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='video-title'>🎥 Detecção de Pragas por Vídeo</div>", unsafe_allow_html=True)
    st.markdown("<div class='video-subtitle'>Faça upload de um vídeo para detectar pragas em todo o conteúdo</div>", unsafe_allow_html=True)

    uploaded_video = st.file_uploader("📤 Fazer Upload de um Vídeo", type=["mp4", "avi", "mov"])

    if uploaded_video:
        pest_info_df = load_pest_info()
        if pest_info_df.empty:
            st.markdown("<div class='status-message status-warning'>⚠️ Arquivo de informações sobre pragas ausente ou vazio.</div>", unsafe_allow_html=True)
            return

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        cap = cv2.VideoCapture(tfile.name)

        stframe = st.empty()
        st.markdown("<div class='status-message status-info'>🔄 Processando vídeo com detecção de pragas...</div>", unsafe_allow_html=True)

        detected_pests = {}
        frame_count = 0
        frame_skip = 5  # Process 1 frame out of 5

        progress_bar = st.progress(0)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue

            frame = cv2.resize(frame, (640, 640))
            results = model(frame)
            annotated = results[0].plot()

            with stframe.container():
                st.markdown("<div class='video-container'>", unsafe_allow_html=True)
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
                        if name not in detected_pests or score > detected_pests[name]:
                            detected_pests[name] = score

            progress = min(frame_count / total_frames, 1.0)
            progress_bar.progress(progress)

        cap.release()
        progress_bar.empty()
        st.markdown("<div class='status-message status-success'>✅ Processamento concluído. Resultados:</div>", unsafe_allow_html=True)

        if detected_pests:
            st.markdown("<div class='pest-results'>", unsafe_allow_html=True)
            for pest, score in detected_pests.items():
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
        else:
            st.markdown("<div class='status-message status-success'>✅ Nenhuma praga detectada com confiança acima de 70%.</div>", unsafe_allow_html=True)
