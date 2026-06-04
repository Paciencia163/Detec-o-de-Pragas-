import streamlit as st

def show():
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

    @keyframes slideInRight {
        0% { opacity: 0; transform: translateX(30px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    .title {
        font-size: 56px;
        text-align: center;
        background: linear-gradient(135deg, #1e5631 0%, #40916c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 30px 0;
        font-weight: 700;
        letter-spacing: 1px;
        animation: fadeIn 0.8s ease;
    }

    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #6b7280;
        margin-bottom: 40px;
        animation: fadeIn 1s ease;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 20px;
        margin-bottom: 40px;
        animation: fadeIn 1.2s ease;
    }

    .feature-card {
        background: linear-gradient(135deg, rgba(64, 145, 108, 0.1) 0%, rgba(82, 183, 136, 0.05) 100%);
        border: 2px solid rgba(64, 145, 108, 0.2);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        animation: slideInRight 0.8s ease backwards;
    }

    .feature-card:nth-child(1) { animation-delay: 0.1s; }
    .feature-card:nth-child(2) { animation-delay: 0.2s; }
    .feature-card:nth-child(3) { animation-delay: 0.3s; }

    .feature-card:hover {
        border-color: #40916c;
        background: linear-gradient(135deg, rgba(64, 145, 108, 0.2) 0%, rgba(82, 183, 136, 0.1) 100%);
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(64, 145, 108, 0.2);
    }

    .feature-card h3 {
        font-size: 24px;
        color: #1e5631;
        margin: 15px 0;
        font-weight: 700;
    }

    .feature-card p {
        color: #6b7280;
        font-size: 16px;
        line-height: 1.6;
    }

    .content-box {
        background: white;
        border-radius: 16px;
        padding: 40px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #40916c;
        animation: slideInLeft 0.8s ease;
    }

    .content-box h2 {
        color: #1e5631;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 2px solid #e5e7eb;
    }

    .content-box ul {
        font-size: 18px;
        line-height: 2;
        color: #374151;
    }

    .content-box li {
        margin-bottom: 12px;
        padding-left: 10px;
        border-left: 3px solid #52b788;
        padding-left: 15px;
    }

    .content-box li b {
        color: #1e5631;
    }

    hr {
        border: none;
        border-top: 2px solid #e5e7eb;
        margin: 30px 0;
    }

    .hero-image {
        border-radius: 16px;
        box-shadow: 0 15px 40px rgba(64, 145, 108, 0.2);
        margin: 30px 0;
        overflow: hidden;
        animation: fadeIn 1.5s ease;
    }

    .hero-image img {
        width: 100%;
        height: auto;
        display: block;
    }

    @media (max-width: 768px) {
        .feature-grid {
            grid-template-columns: 1fr;
        }

        .title {
            font-size: 36px;
        }

        .content-box {
            padding: 25px;
        }

        .content-box h2 {
            font-size: 22px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>🌾 Bem-vindo ao Kulima 🌾</div>\n<div class='subtitle'>Detecção Inteligente de Pragas Agrícolas com IA</div>", unsafe_allow_html=True)

    # Hero Image
    st.markdown("""
    <div class='hero-image'>
        <img src="https://images.pexels.com/photos/1072824/pexels-photo-1072824.jpeg?auto=compress&cs=tinysrgb&w=1200">
    </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    st.markdown("""
    <div class='feature-grid'>
        <div class='feature-card'>
            <div style='font-size: 48px; margin-bottom: 10px;'>📸</div>
            <h3>Detecção por Imagem</h3>
            <p>Analise suas colheitas instantaneamente com upload de fotos</p>
        </div>
        <div class='feature-card'>
            <div style='font-size: 48px; margin-bottom: 10px;'>🎥</div>
            <h3>Detecção por Vídeo</h3>
            <p>Processe vídeos para detecção automática quadro a quadro</p>
        </div>
        <div class='feature-card'>
            <div style='font-size: 48px; margin-bottom: 10px;'>📹</div>
            <h3>Tempo Real</h3>
            <p>Monitoramento em tempo real via webcam da sua fazenda</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Content
    st.markdown("""
    <div class='content-box'>
        <h2>🚀 Recursos Principais</h2>
        <ul>
            <li><b>Detecção de Pragas Precisa:</b> Identifique pragas agrícolas com precisão utilizando tecnologia de visão computacional.</li>
            <li><b>Recomendações Personalizadas:</b> Receba sugestões de fertilizantes e soluções adaptadas às suas culturas.</li>
            <li><b>Interface Intuitiva:</b> Fácil de usar, sem necessidade de conhecimento técnico prévio.</li>
            <li><b>Processamento Rápido:</b> Resultados instantâneos para tomadas de decisão ágeis.</li>
        </ul>
    </div>

    <div class='content-box' style='border-left-color: #f77f00; margin-top: 30px;'>
        <h2>⚡ Tecnologia por Trás</h2>
        <ul>
            <li><b>Modelo YOLO v8:</b> Redes neurais de última geração para detecções ultra-precisas e rápidas.</li>
            <li><b>Streamlit:</b> Interface web moderna e responsiva para melhor experiência do usuário.</li>
            <li><b>OpenCV:</b> Processamento avançado de imagens e vídeos em tempo real.</li>
            <li><b>Inteligência Artificial:</b> Machine Learning para otimização contínua do sistema.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
