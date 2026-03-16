import streamlit as st

def show():
    st.markdown("""
    <style>
    .title {
        font-size: 42px;
        text-align: center;
        color: #4CAF50;
        padding: 20px 0;
    }
    .content-box {
        background-color: #f9f9f9;
        border-radius: 12px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    h2 {
        color: #2E7D32;
    }
    ul {
        font-size: 18px;
        line-height: 1.8;
    }
    hr {
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>🌿 Bem-vindo ao FarmWise: Detecção Inteligente para Agricultura 🌿</div>", unsafe_allow_html=True)

    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXHsvQ31b86uvV1PYVF22DWMK8g9jY9wyzw_jbmbKuO5FpKZcME7bSBXtF0rB9HMIvRYo&usqp=CAU",
        use_container_width=True
    )

    st.markdown("""
    <div class='content-box'>
        <h2>🚀 O que você pode fazer</h2>
        <ul>
            <li>📸 <b>Faça upload de imagens</b> para detectar pragas instantaneamente.</li>
            <li>🎬 <b>Faça upload de vídeos</b> para detecção automática de pragas quadro a quadro.</li>
            <li>📹 <b>Use sua webcam</b> para detecção inteligente de pragas em tempo real!</li>
        </ul>
        <hr>
        <h2>✅ Desenvolvido com</h2>
        <ul>
            <li>⚡ <b>Modelo YOLO</b> para detecções rápidas e precisas</li>
            <li>🖥️ <b>Streamlit</b> para uma experiência web suave</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
