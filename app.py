import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Private Bank | Multi-Ativos", layout="wide")

# Estilo Dark Mode Premium
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS (SUA CARTEIRA DE FIIs) ---
carteira_fiis = {
    "MXRF11": 2001.24, "RECR11": 2090.66, "VGHF11": 3009.60,
    "VISC11": 2097.03, "XPML11": 3448.44, "BTCI11": 2008.10,
    "HGLG11": 5037.76, "KNCR11": 10080.45
}

# Outros Investimentos (Ajuste conforme necessário)
outros_invest = {
    "Tesouro SELIC 2029": 5000.00,
    "CDB Pós-Fixado (110% CDI)": 8000.00
}

# --- CÁLCULOS ---
total_patrimonio = sum(carteira_fiis.values()) + sum(outros_invest.values())

# --- CABEÇALHO ---
st.title("🏛 Private Bank - Dashboard Global")
st.write(f"Sincronizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- DASHBOARD DE INDICADORES ---
c1, c2, c3 = st.columns(3)
c1.metric("Patrimônio Total", f"R$ {total_patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Total em FIIs", f"R$ {sum(carteira_fiis.values()):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c3.metric("Renda Fixa / Tesouro", f"R$ {sum(outros_invest.values()):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- MONITOR DE CRIPTOMOEDAS (Apenas Cotação) ---
st.markdown("### ₿ Radar de Criptomoedas (Mercado Global)")
col_crypto = st.columns(4)

cryptos_monitor = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"]
for i, ticker in enumerate(cryptos_monitor):
    data = yf.Ticker(ticker).fast_info
    preco = data['last_price']
    variacao = ((preco / data['previous_close']) - 1) * 100
    col_crypto[i].metric(ticker.replace("-USD", ""), f"US$ {preco:,.2f}", f"{variacao:.2f}%")

st.markdown("---")

# --- GRÁFICOS E NOTÍCIAS EM TEMPO REAL ---
col_esq, col_dir = st.columns([1.5, 1])

with col_esq:
    st.markdown("### 📊 Minha Alocação de Ativos")
    # Une os dados para o gráfico
    dados_grafico = {**carteira_fiis, **outros_invest}
    df = pd.DataFrame(list(dados_grafico.items()), columns=['Ativo', 'Valor'])
    fig = px.pie(df, values='Valor', names='Ativo', hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig, use_container_width=True)

with col_dir:
    st.markdown("### 📰 Notícias em Tempo Real")
    try:
        # Busca notícias globais via Yahoo Finance
        feed = yf.Ticker("^BVSP").news[:6] 
        for n in feed:
            st.info(f"**{n['title']}**")
            st.caption(f"[Ler notícia completa]({n['link']})")
    except:
        st.write("Atualizando feed de notícias...")

# --- TABELA DE CONTROLE ---
with st.expander("👁 Ver Detalhamento"):
    df_full = pd.DataFrame(list(carteira_fiis.items()) + list(outros_invest.items()), columns=['Ativo', 'Saldo (R$)'])
    st.table(df_full.style.format({'Saldo (R$)': 'R$ {:.2f}'}))
