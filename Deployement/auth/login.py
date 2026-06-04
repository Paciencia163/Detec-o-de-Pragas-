import streamlit as st
from auth.auth_utils import init_db, verify_user, add_user, user_exists

def login_screen():
    init_db()  # Ensure DB is initialized

    # --- CSS Animations and Styling ---
    st.markdown("""
    <style>
    @keyframes fadeIn {
      0% { opacity: 0; transform: translateY(-20px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInUp {
      0% { opacity: 0; transform: translateY(30px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes shake {
      0% { transform: translateX(0); }
      25% { transform: translateX(-5px); }
      50% { transform: translateX(5px); }
      75% { transform: translateX(-5px); }
      100% { transform: translateX(0); }
    }

    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(64, 145, 108, 0.7); }
      70% { box-shadow: 0 0 0 15px rgba(64, 145, 108, 0); }
      100% { box-shadow: 0 0 0 0 rgba(64, 145, 108, 0); }
    }

    * {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    body {
      background: linear-gradient(135deg, #1e5631 0%, #40916c 50%, #52b788 100%);
      min-height: 100vh;
    }

    .login-container {
      background: white;
      border-radius: 20px;
      padding: 50px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
      max-width: 500px;
      margin: 50px auto;
      animation: slideInUp 0.8s ease;
    }

    .login-title {
        text-align: center;
        font-size: 48px;
        background: linear-gradient(135deg, #1e5631 0%, #40916c 100%);\n        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        animation: fadeIn 1s ease-in;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .login-subtitle {
        text-align: center;
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 40px;
        animation: fadeIn 1.2s ease-in;
    }

    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 16px 20px !important;
        margin-bottom: 20px !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #40916c !important;
        box-shadow: 0 0 0 3px rgba(64, 145, 108, 0.1) !important;
    }

    .stButton > button {
        font-size: 18px;
        font-weight: 600;
        padding: 14px 28px !important;
        background: linear-gradient(135deg, #40916c 0%, #52b788 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(64, 145, 108, 0.3) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #52b788 0%, #74c69d 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(64, 145, 108, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .error {
        animation: shake 0.5s;
    }

    .agri-images {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
        animation: fadeIn 1.5s ease;
    }

    .agri-images img {
        width: 140px;
        height: 140px;
        object-fit: cover;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }

    .agri-images img:hover {
        transform: scale(1.05);
    }

    [role=\"radiogroup\"] {
        display: flex !important;
        gap: 15px !important;
        margin: 25px 0 !important;
    }

    [role=\"radiogroup\"] > label {
        flex: 1 !important;
        padding: 14px 20px !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        color: #374151 !important;
        background: #f9fafb !important;
    }

    [role=\"radiogroup\"] > label:hover {
        border-color: #40916c !important;
        background: #f0f9f7 !important;
    }

    [role=\"radiogroup\"] > label[data-selected=\"true\"] {
        background: linear-gradient(135deg, #40916c 0%, #52b788 100%) !important;
        color: white !important;
        border-color: #40916c !important;
    }

    .warning-box, .success-box {
        border-radius: 12px !important;
        padding: 16px !important;
        margin: 15px 0 !important;
        animation: slideInUp 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Title ---
    st.markdown("<div class='login-title'>🌾 Kulima</div>\n<div class='login-subtitle'>Detecção Inteligente de Pragas para Agricultura</div>", unsafe_allow_html=True)

    # --- Agriculture Images ---
    st.markdown("""
    <div class='agri-images'>
        <img src="https://images.pexels.com/photos/1072824/pexels-photo-1072824.jpeg?auto=compress&cs=tinysrgb&w=600">
        <img src="https://images.pexels.com/photos/2255920/pexels-photo-2255920.jpeg?auto=compress&cs=tinysrgb&w=600">
        <img src="https://images.pexels.com/photos/247616/pexels-photo-247616.jpeg?auto=compress&cs=tinysrgb&w=600">
    </div>
    """, unsafe_allow_html=True)

    # --- Toggle between login and register ---
    page = st.radio("Escolha uma opção:", ["🔐 Entrar", "📝 Criar Conta"], horizontal=True)

    # --- Input Fields ---
    username = st.text_input("👤 Nome de Usuário")
    password = st.text_input("🔑 Senha", type="password")

    if page == "🔐 Entrar":
        if st.button("🔓 Entrar"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.success("✅ Login bem-sucedido! Redirecionando...")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Nome de usuário ou senha inválidos.")
                st.markdown("<div class='error'></div>", unsafe_allow_html=True)
    else:
        confirm_password = st.text_input("🔁 Confirmar Senha", type="password")
        if st.button("🆕 Criar Conta"):
            if user_exists(username):
                st.warning("⚠️ Nome de usuário já existe.")
            elif password != confirm_password:
                st.warning("⚠️ As senhas não coincidem.")
            elif not username or not password:
                st.warning("⚠️ Todos os campos são obrigatórios.")
            else:
                add_user(username, password)
                st.success("✅ Conta criada com sucesso! Por favor, faça login.")
