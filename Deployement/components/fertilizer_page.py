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
    st.title("🌾 Recomendação de Fertilizante")
    st.markdown("Obtenha o fertilizante mais adequado com base nos dados do seu solo e cultura.")

    # User inputs
    N = st.slider("Nitrogênio (N)", 0, 140, 34)
    P = st.slider("Fósforo (P)", 5, 145, 65)
    K = st.slider("Potássio (K)", 5, 205, 62)
    temp = st.slider("Temperatura (°C)", 0, 50, 30)
    humidity = st.slider("Umidade (%)", 0, 100, 65)
    moisture = st.slider("Umidade do Solo (%)", 0, 100, 7)
    soil_type = st.selectbox("Tipo de Solo", ["Black", "Clayey", "Loamy", "Red", "Sandy"])
    crop_type = st.selectbox("Tipo de Cultura", ["Barley", "Cotton", "Ground Nuts", "Maize", "Millets", "Oil seeds", "Paddy", "Pulses", "Sugarcane", "Tobacco", "Wheat"])

    # Encode categorical values
    soil_dict = {"Black": 0, "Clayey": 1, "Loamy": 2, "Red": 3, "Sandy": 4}
    crop_dict = {
        "Barley": 0, "Cotton": 1, "Ground Nuts": 2, "Maize": 3, "Millets": 4,
        "Oil seeds": 5, "Paddy": 6, "Pulses": 7, "Sugarcane": 8, "Tobacco": 9, "Wheat": 10
    }

    if st.button("Prever Fertilizante"):
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

        predicted_fertilizer = fertilizer_mapping.get(ans[0], "Unknown")

        # Get more info
        row = info[info['Fertilizer Name'].str.replace('/', '-').str.strip() == predicted_fertilizer]

        st.subheader("🌿 Fertilizante Recomendado:")
        st.success(predicted_fertilizer)

        if not row.empty:
            st.markdown(f"**🔍 Descrição:** {row.iloc[0]['Description']}")
            st.markdown(f"**🌱 Melhor Usado Para:** {row.iloc[0]['Best Used For']}")
            st.markdown(f"**💡 Aplicação:** {row.iloc[0]['Application']}")
        else:
            st.warning("⚠️ Informações sobre fertilizante não encontradas no CSV.")
