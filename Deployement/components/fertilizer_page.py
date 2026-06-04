import streamlit as st
import pandas as pd
import pickle
import os


# Load the model and data once
@st.cache_resource
def load_fertilizer_model():
    model_path = os.path.join("model", "fertilizer.pkl")
    with open(model_path, "rb") as file:
        return pickle.load(file)

@st.cache_data
def load_fertilizer_info():
    csv_path = os.path.join("utils", "fertilizer_instructions.csv")
    return pd.read_csv(csv_path)

def show_fertilizer_page():
    st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInLeft {
        0% { opacity: 0; transform: translateX(-30px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    .fertilizer-title {
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

    .fertilizer-subtitle {
        text-align: center;
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 40px;
        animation: fadeIn 1s ease;
    }

    .input-section {
        background: white;
        border-radius: 16px;
        padding: 35px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #40916c;
        animation: slideInLeft 0.8s ease;
    }

    .input-group {
        margin-bottom: 25px;
    }

    .input-group label {
        font-weight: 600;
        color: #1e5631;
        margin-bottom: 8px;
        display: block;
        font-size: 15px;
    }

    .slider-value {
        font-size: 14px;
        color: #40916c;
        font-weight: 600;
        margin-top: 5px;
    }

    .form-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    .prediction-result {
        background: linear-gradient(135deg, #1e5631 0%, #40916c 100%);
        color: white;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 15px 40px rgba(64, 145, 108, 0.3);
        animation: fadeIn 0.8s ease;
    }

    .result-label {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        opacity: 0.9;
    }

    .result-value {
        font-size: 52px;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .fertilizer-details {
        background: white;
        border-radius: 16px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #f77f00;
        animation: slideInLeft 0.8s ease 0.2s backwards;
    }

    .fertilizer-details h3 {
        color: #1e5631;
        font-weight: 700;
        margin-top: 0;
        font-size: 24px;
    }

    .detail-row {
        padding: 12px 0;
        border-bottom: 1px solid #e5e7eb;
    }

    .detail-row:last-child {
        border-bottom: none;
    }

    .detail-label {
        font-weight: 600;
        color: #1e5631;
        display: block;
        margin-bottom: 5px;
    }

    .detail-value {
        color: #6b7280;
        font-size: 15px;
        line-height: 1.6;
    }

    .action-button {
        background: linear-gradient(135deg, #40916c 0%, #52b788 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 16px 32px !important;
        border: none !important;
        border-radius: 12px !important;
        width: 100% !important;
        margin-top: 20px !important;
        box-shadow: 0 8px 20px rgba(64, 145, 108, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .action-button:hover {
        background: linear-gradient(135deg, #52b788 0%, #74c69d 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(64, 145, 108, 0.4) !important;
    }

    .stSelectbox > div > div {
        border-radius: 8px !important;
    }

    .warning-message {
        background: rgba(255, 193, 7, 0.1);
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        color: #f57f17;
        font-weight: 600;
        margin: 20px 0;
    }

    @media (max-width: 768px) {
        .form-columns {
            grid-template-columns: 1fr;
        }

        .fertilizer-title {
            font-size: 36px;
        }

        .result-value {
            font-size: 36px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='fertilizer-title'>🌾 Recomendação de Fertilizante</div>", unsafe_allow_html=True)
    st.markdown("<div class='fertilizer-subtitle'>Obtenha o fertilizante ideal com base nos dados do seu solo e cultura</div>", unsafe_allow_html=True)

    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='input-group'><label>Nitrogênio (N) - ppm</label>", unsafe_allow_html=True)
        N = st.slider("", 0, 140, 34, label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>Valor: {N}</div></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='input-group'><label>Fósforo (P) - ppm</label>", unsafe_allow_html=True)
        P = st.slider("", 5, 145, 65, key="p_slider", label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>Valor: {P}</div></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='input-group'><label>Potássio (K) - ppm</label>", unsafe_allow_html=True)
        K = st.slider("", 5, 205, 62, key="k_slider", label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>Valor: {K}</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='input-group'><label>Temperatura (°C)</label>", unsafe_allow_html=True)
        temp = st.slider("", 0, 50, 30, key="temp_slider", label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>Valor: {temp}°C</div></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='input-group'><label>Umidade Relativa (%)</label>", unsafe_allow_html=True)
        humidity = st.slider("", 0, 100, 65, key="humidity_slider", label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>Valor: {humidity}%</div></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='input-group'><label>Umidade do Solo (%)</label>", unsafe_allow_html=True)
        moisture = st.slider("", 0, 100, 7, key="moisture_slider", label_visibility="collapsed")
        st.markdown(f"<div class='slider-value'>Valor: {moisture}%</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        soil_type = st.selectbox("Tipo de Solo", ["Black", "Clayey", "Loamy", "Red", "Sandy"])
    with col2:
        crop_type = st.selectbox("Tipo de Cultura", ["Barley", "Cotton", "Ground Nuts", "Maize", "Millets", "Oil seeds", "Paddy", "Pulses", "Sugarcane", "Tobacco", "Wheat"])

    # Encode categorical values
    soil_dict = {"Black": 0, "Clayey": 1, "Loamy": 2, "Red": 3, "Sandy": 4}
    crop_dict = {
        "Barley": 0, "Cotton": 1, "Ground Nuts": 2, "Maize": 3, "Millets": 4,
        "Oil seeds": 5, "Paddy": 6, "Pulses": 7, "Sugarcane": 8, "Tobacco": 9, "Wheat": 10
    }

    if st.button("🔮 Prever Fertilizante Ideal", use_container_width=True):
        model = load_fertilizer_model()
        info = load_fertilizer_info()
        
        # Predict
        input_data = [[N, P, K, soil_dict[soil_type], crop_dict[crop_type], temp, humidity, moisture]]
        ans = model.predict(input_data)

        fertilizer_mapping = {
            0: "10-26-26",
            1: "14-35-14",
            2: "17-17-17",
            3: "20-20",
            4: "28-28",
            5: "DAP",
            6: "Urea"
        }

        predicted_fertilizer = fertilizer_mapping.get(ans[0], "Desconhecido")

        # Get more info
        row = info[info['Fertilizer Name'].str.replace('/', '-').str.strip() == predicted_fertilizer]

        st.markdown(f"""
        <div class='prediction-result'>
            <div class='result-label'>🌱 Fertilizante Recomendado</div>
            <div class='result-value'>{predicted_fertilizer}</div>
        </div>
        """, unsafe_allow_html=True)

        if not row.empty:
            st.markdown(f"""
            <div class='fertilizer-details'>
                <h3>📋 Informações do Fertilizante</h3>
                <div class='detail-row'>
                    <span class='detail-label'>📖 Descrição</span>
                    <div class='detail-value'>{row.iloc[0]['Description']}</div>
                </div>
                <div class='detail-row'>
                    <span class='detail-label'>🌾 Melhor Usado Para</span>
                    <div class='detail-value'>{row.iloc[0]['Best Used For']}</div>
                </div>
                <div class='detail-row'>
                    <span class='detail-label'>💡 Aplicação</span>
                    <div class='detail-value'>{row.iloc[0]['Application']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='warning-message'>⚠️ Informações sobre fertilizante não encontradas na base de dados.</div>", unsafe_allow_html=True)
