import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Private Bank Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Estilização CSS para visual de Banco (Dark Mode & Cards)
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stMetric { background-color: #1E1E1E; padding: 20px; border-radius: 15px; border-left: 5px solid #2ecc71; }
    div[data-testid="stMetricValue"] { color: #2ecc71; font-size: 28px; }
    .stAppHeader { background-color: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DA CARTEIRA (R$ 29.773,28) ---
carteira = {
    "MXRF11": 2001.24, "RECR11": 2090.66, "VGHF11": 3009.60,
    "VISC11": 2097.03, "XPML11": 3448.44, "BTCI11": 2008.10,
    "HGLG11": 5037.76, "KNCR11": 10080.45
}

# --- CÁLCULOS ---
total_patrimonio = sum(carteira.values())
dividendos_est = total_patrimonio * 0.0095 # Estimativa 0.95% am

# --- CABEÇALHO ---
st.title("🏛 Private Bank - Dashboard")
st.subheader(f"Bem-vindo de volta! | {datetime.now().strftime('%d/%m/%Y')}")

# --- DASHBOARD LAYOUT ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Patrimônio Total", f"R$ {total_patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col2:
    st.metric("Dividendos Estimados (Mês)", f"R$ {dividendos_est:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col3:
    st.metric("Yield Médio", "0,95% a.m.")

st.markdown("---")

# --- GRÁFICOS INTERATIVOS ---
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown("### 📊 Alocação de Ativos")
    df_pizza = pd.DataFrame(list(carteira.items()), columns=['Ticker', 'Valor'])
    fig_pizza = px.pie(df_pizza, values='Valor', names='Ticker', hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Greens_r)
    fig_pizza.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pizza, use_container_width=True)

with c2:
    st.markdown("### 📰 Notícias do Mercado")
    try:
        news = yf.Ticker("^BVSP").news[:5]
        for n in news:
            st.info(f"**{n['title']}**")
            st.caption(f"[Ler notícia completa]({n['link']})")
    except:
        st.write("Notícias indisponíveis no momento.")

# --- TABELA DETALHADA ---
st.markdown("### 📋 Detalhamento da Carteira")
df_table = pd.DataFrame(list(carteira.items()), columns=['FII', 'Saldo Atual (R$)'])
st.dataframe(df_table.style.format({"Saldo Atual (R$)": "R$ {:.2f}"}), use_container_width=True)
