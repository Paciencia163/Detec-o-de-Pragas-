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
    st.markdown("<h1 style='text-align:center;'>🪰 Detecção de Pragas</h1>", unsafe_allow_html=True)
    st.markdown("Faça upload de uma imagem para identificar pragas prejudiciais.")

    uploaded_file = st.file_uploader("📤 Fazer Upload de Imagem", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        st.image(image, caption="📷 Imagem Carregada", channels="BGR", use_container_width=True)

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
                    st.subheader("🔍 Resultados da Detecção")
                    pest_info_df = load_pest_info()

                    if pest_info_df.empty:
                        st.warning("⚠️ Não foi possível carregar dados de referência sobre pragas.")
                    else:
                        for pest, score in top_pests.items():
                            st.markdown(f"### 🐞 {pest} ✅")
                            st.markdown(f"**Confiança:** {score * 100:.2f}%")

                            row = pest_info_df[pest_info_df["Pest Name"].str.lower() == pest.lower()]
                            if not row.empty:
                                st.markdown(f"**🔬 Nome Científico:** *{row.iloc[0]['Scientific Name']}*")
                                st.markdown(f"**📖 Descrição:**\n> {row.iloc[0]['Description']}")
                                st.markdown(f"**🛠️ Estratégias de Manejo:**\n- {row.iloc[0]['Management Strategies']}")
                            else:
                                st.warning("📄 Nenhuma informação detalhada encontrada no CSV para esta praga.")
                            st.markdown("---")
                else:
                    st.info("✅ Nenhuma praga detectada com confiança superior a 70%.")
            else:
                st.info("📭 Nenhuma praga detectada nesta imagem.")

        st.image(annotated_img, caption="📌 Resultado Anotado", channels="BGR", use_container_width=True)
