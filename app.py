import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Private Bank Dashboard", layout="wide")

# Estilização Dark Mode
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #2ecc71; }
    </style>
    """, unsafe_allow_html=True)

# --- SEU PATRIMÔNIO REAL (FIXO: R$ 29.773,28) ---
carteira_fiis = {
    "MXRF11": 2001.24, "RECR11": 2090.66, "VGHF11": 3009.60,
    "VISC11": 2097.03, "XPML11": 3448.44, "BTCI11": 2008.10,
    "HGLG11": 5037.76, "KNCR11": 10080.45
}
total_investido = sum(carteira_fiis.values()) # Soma exata: 29.773,28

# --- CABEÇALHO ---
st.title("🏛 Private Bank - Dashboard Profissional")
st.write(f"📊 Consolidado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- DASHBOARD DE INDICADORES (SEU VALOR REAL) ---
c1, c2, c3 = st.columns(3)
c1.metric("Patrimônio Total", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Classe Principal", "FIIs (100%)")
c3.metric("Dividendos Est. (Mês)", f"R$ {total_investido * 0.0096:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- MONITOR DE MERCADO (APENAS PARA ACOMPANHAR) ---
st.markdown("### ⚡ Radar de Mercado (Cripto & Índices)")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

# Lista de ativos para monitorar sem investir
ativos_monitor = ["BTC-USD", "ETH-USD", "^BVSP", "USDBRL=X"]
nomes_monitor = ["Bitcoin", "Ethereum", "Ibovespa", "Dólar"]

for i, ticker in enumerate(ativos_monitor):
    try:
        dados = yf.Ticker(ticker).fast_info
        preco = dados['last_price']
        var = ((preco / dados['previous_close']) - 1) * 100
        prefixo = "US$ " if "USD" in ticker else "R$ " if "BRL" in ticker else ""
        col_m1, col_m2, col_m3, col_m4 = [col_m1, col_m2, col_m3, col_m4] # Garante ordem
        locals()[f"col_m{i+1}"].metric(nomes_monitor[i], f"{prefixo}{preco:,.2f}", f"{var:.2f}%")
    except: pass

st.markdown("---")

# --- GRÁFICOS E NOTÍCIAS EM TEMPO REAL ---
col_graf, col_news = st.columns([1.5, 1])

with col_graf:
    st.markdown("### 📊 Alocação da Carteira")
    df = pd.DataFrame(list(carteira_fiis.items()), columns=['FII', 'Valor'])
    fig = px.pie(df, values='Valor', names='FII', hole=0.5, 
                 color_discrete_sequence=px.colors.sequential.Greens_r)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col_news:
    st.markdown("### 📰 Notícias em Tempo Real")
    try:
        # Busca notícias globais e do Brasil
        feed = yf.Ticker("^BVSP").news[:5]
        for n in feed:
            st.info(f"**{n['title']}**")
            st.caption(f"[Ler notícia completa]({n['link']})")
    except:
        st.write("Conectando ao feed de notícias...")

# --- TABELA DE CONTROLE ---
with st.expander("👁 Ver Detalhamento dos Ativos"):
    df_tab = pd.DataFrame(list(carteira_fiis.items()), columns=['Ticker', 'Saldo Atual'])
    st.table(df_tab.style.format({'Saldo Atual': 'R$ {:.2f}'}))
