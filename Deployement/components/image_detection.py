import streamlit as st
import numpy as np
import cv2
import pandas as pd

# Optimized loading of the CSV file containing pest information
@st.cache_data
def load_pest_info():
    try:
        pest_info = pd.read_csv(r"utils\detailed_pests_solutions.csv")
        return pest_info
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return pd.DataFrame()

# Main detection function
def show(model):
    st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .image-detection-title {
        font-size: 42px;
        text-align: center;
        color: #1e5631;
        font-weight: 700;
        margin-bottom: 10px;
        animation: fadeIn 0.8s ease;
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 30px;
        animation: fadeIn 1s ease;
    }

    .upload-area {
        border: 2px dashed #40916c;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        background: rgba(64, 145, 108, 0.05);
        transition: all 0.3s ease;
    }

    .upload-area:hover {
        background: rgba(64, 145, 108, 0.1);
        border-color: #52b788;
    }

    .image-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }

    .results-box {
        background: linear-gradient(135deg, rgba(64, 145, 108, 0.1) 0%, rgba(82, 183, 136, 0.05) 100%);
        border-left: 5px solid #40916c;
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
        animation: fadeIn 0.8s ease;
    }

    .pest-card {
        background: white;
        border-left: 4px solid #f77f00;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .pest-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }

    .pest-card h3 {
        color: #1e5631;
        margin-top: 0;
        font-weight: 700;
    }

    .confidence-bar {
        background: #e5e7eb;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin: 10px 0;
    }

    .confidence-fill {
        background: linear-gradient(90deg, #40916c 0%, #52b788 100%);
        height: 100%;
        transition: width 0.3s ease;
    }

    .info-row {
        margin: 12px 0;
        padding: 10px;
        border-left: 3px solid #40916c;
        padding-left: 15px;
    }

    .info-row strong {
        color: #1e5631;
    }

    .spinner-text {
        color: #40916c;
        font-weight: 600;
    }

    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 25px 0;
    }

    .success-message {
        background: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4caf50;
        padding: 15px;
        border-radius: 8px;
        color: #2e7d32;
        font-weight: 600;
    }

    .warning-message {
        background: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        color: #f57f17;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='image-detection-title'>🪰 Detecção de Pragas por Imagem</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Faça upload de uma imagem para identificar pragas prejudiciais</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📤 Fazer Upload de Imagem", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class='image-container'>""", unsafe_allow_html=True)
            st.image(image, caption="📷 Imagem Carregada", channels="BGR", use_container_width=True)
            st.markdown("""</div>""", unsafe_allow_html=True)

        with st.spinner("🔎 Analisando imagem..."):
            results = model(image)
            annotated_img = results[0].plot()
            names = results[0].names
            probs = results[0].probs

            if probs is not None and len(probs) > 0:
                probs_data = probs.data.cpu().numpy()
                pest_scores = {names[i]: float(probs_data[i]) for i in range(len(probs_data))}
                sorted_pests = dict(sorted(pest_scores.items(), key=lambda item: item[1], reverse=True))

                # Only keep pests with confidence >= 70%
                top_pests = {pest: score for pest, score in sorted_pests.items() if score >= 0.7}

                if top_pests:
                    with col2:
                        st.markdown("""<div class='image-container'>""", unsafe_allow_html=True)
                        st.image(annotated_img, caption="📌 Resultado Anotado", channels="BGR", use_container_width=True)
                        st.markdown("""</div>""", unsafe_allow_html=True)

                    st.markdown("<div class='results-box'><h2 style='color:#1e5631; margin-top:0;'>🔍 Resultados da Detecção</h2>", unsafe_allow_html=True)
                    pest_info_df = load_pest_info()

                    if pest_info_df.empty:
                        st.warning("⚠️ Não foi possível carregar dados de referência sobre pragas.")
                    else:
                        for pest, score in top_pests.items():
                            st.markdown(f"""
                            <div class='pest-card'>
                                <h3>🐞 {pest} ✅</h3>
                                <div class='info-row'><strong>Confiança:</strong> {score * 100:.2f}%</div>
                            """, unsafe_allow_html=True)

                            row = pest_info_df[pest_info_df["Pest Name"].str.lower() == pest.lower()]
                            if not row.empty:
                                st.markdown(f"<div class='info-row'><strong>🔬 Nome Científico:</strong> <em>{row.iloc[0]['Scientific Name']}</em></div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='info-row'><strong>📖 Descrição:</strong><br>{row.iloc[0]['Description']}</div>", unsafe_allow_html=True)
                                st.markdown(f"<div class='info-row'><strong>🛠️ Estratégias de Manejo:</strong><br>{row.iloc[0]['Management Strategies']}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown("<div class='warning-message'>📄 Nenhuma informação detalhada encontrada no banco de dados para esta praga.</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='success-message'>✅ Nenhuma praga detectada com confiança superior a 70%.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='warning-message'>📭 Nenhuma praga detectada nesta imagem.</div>", unsafe_allow_html=True)
