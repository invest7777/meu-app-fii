import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Private Bank | Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
    }
    div[data-testid="stMetricValue"] { color: #2ecc71; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #2ecc71; }
    .stAppHeader { background-color: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DA CARTEIRA ---
fiis = {"MXRF11": 2001.24, "RECR11": 2090.66, "VGHF11": 3009.60, "VISC11": 2097.03, "XPML11": 3448.44, "BTCI11": 2008.10, "HGLG11": 5037.76, "KNCR11": 10080.45}
cryptos = {"BTC-BRL": 4500.00, "ETH-BRL": 1500.00}
renda_fixa = {"Tesouro SELIC": 5000.00, "CDB 110% CDI": 3000.00}

total_geral = sum(fiis.values()) + sum(cryptos.values()) + sum(renda_fixa.values())
meta_objetivo = 100000.00
progresso = min(total_geral / meta_objetivo, 1.0)

# --- CABEÇALHO ---
st.title("🏛 Corretora Private - Global Dashboard")
st.caption(f"📍 Conectado via API B3/Yahoo | {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- BARRA DE PROGRESSO (META R$ 100K) ---
col_meta1, col_meta2 = st.columns([4, 1])
with col_meta1:
    st.write(f"🎯 **Meta de Patrimônio: R$ {meta_objetivo:,.2f}**")
    st.progress(progresso)
with col_meta2:
    st.write(f"📊 **{progresso*100:.1f}% concluído**")

st.markdown("---")

# --- LINHA 1: DASHBOARD DE INDICADORES ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Patrimônio Líquido", f"R$ {total_geral:,.2f}")
c2.metric("Proventos Estimados", f"R$ {total_geral*0.0096:,.2f}", delta="Mensal")
c3.metric("Rentabilidade Acumulada", "+1.28%", delta="0.12%")
c4.metric("Ativos em Custódia", len(fiis) + len(cryptos) + len(renda_fixa))

# --- LINHA 2: GRÁFICOS E NOTÍCIAS ---
col_graf, col_news = st.columns([1.5, 1])

with col_graf:
    st.markdown("### 📊 Alocação Estratégica")
    df_classes = pd.DataFrame({
        'Classe': ['FIIs', 'Cripto', 'Renda Fixa'],
        'Valor': [sum(fiis.values()), sum(cryptos.values()), sum(renda_fixa.values())]
    })
    fig = px.pie(df_classes, values='Valor', names='Classe', hole=0.6,
                 color_discrete_sequence=['#2ecc71', '#f1c40f', '#3498db'])
    fig.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col_news:
    st.markdown("### 📰 Market News & Insights")
    try:
        # Busca notícias globais e locais
        noticias = yf.Ticker("^BVSP").news[:5]
        for n in noticias:
            st.info(f"**{n['title']}**")
            st.caption(f"[Acessar Relatório Completo]({n['link']})")
    except:
        st.write("🔄 Atualizando feed de notícias...")

# --- LINHA 3: TABELA DE CUSTÓDIA ---
with st.expander("👁 Visualizar Detalhamento da Carteira"):
    df_full = pd.DataFrame(list(fiis.items()) + list(cryptos.items()) + list(renda_fixa.items()), 
                          columns=['Ativo', 'Saldo (R$)'])
    st.dataframe(df_full.style.format({'Saldo (R$)': 'R$ {:.2f}'}), use_container_width=True)
