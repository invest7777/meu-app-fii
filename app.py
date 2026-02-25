import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="Private Bank | Dashboard", layout="wide", page_icon="🏦")

# CSS Customizado para Visual de Corretora (Dark Mode & Gold)
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-5px); border-color: #F1C40F; }
    div[data-testid="stMetricValue"] { color: #2ECC71 !important; font-size: 30px !important; }
    .stAlert { background-color: #161B22; border: 1px solid #30363D; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SEU PATRIMÔNIO (FIXO: R$ 29.773,28) ---
patrimonio = 29773.28
dividendos = 285.82

# --- CABEÇALHO ---
st.title("🏛️ Banco Privado - Painel Global")
st.caption(f"🕒 Última Sincronização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- LINHA 1: METRICAS PRINCIPAIS ---
c1, c2, c3 = st.columns(3)
c1.metric("💰 Patrimônio Total", f"R$ {patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("📊 Alocação", "FIIs (100%)", delta="Consolidado")
c3.metric("💸 Dividendos Est. (Mês)", f"R$ {dividendos:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- LINHA 2: RADAR DE MERCADO (CRIPTO & INDICES) ---
st.subheader("⚡ Radar de Mercado em Tempo Real")
m1, m2, m3, m4 = st.columns(4)

monitorar = {"BTC-USD": "₿ Bitcoin", "ETH-USD": "Ξ Ethereum", "^BVSP": "📉 Ibovespa", "USDBRL=X": "💵 Dólar"}

for i, (ticker, nome) in enumerate(monitorar.items()):
    try:
        data = yf.Ticker(ticker).fast_info
        preco = data['last_price']
        var = ((preco / data['previous_close']) - 1) * 100
        cols = [m1, m2, m3, m4]
        simbolo = "US$ " if "USD" in ticker else "R$ " if "BRL" in ticker else ""
        cols[i].metric(nome, f"{simbolo}{preco:,.2f}", f"{var:.2f}%")
    except: pass

st.markdown("---")

# --- LINHA 3: NOTICIAS (CORREÇÃO DO FEED) ---
col_news, col_info = st.columns([2, 1])

with col_news:
    st.subheader("📰 Notícias do Mercado (Tempo Real)")
    try:
        # Buscamos do índice principal para garantir que o feed não venha vazio
        news = yf.Ticker("^BVSP").news[:6] 
        if news:
            for n in news:
                with st.container():
                    st.markdown(f"""
                    <div style='background-color: #161B22; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #F1C40F;'>
                        <small style='color: #8B949E;'>{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%H:%M')}</small><br>
                        <strong style='font-size: 16px;'>{n['title']}</strong><br>
                        <a href='{n['link']}' target='_blank' style='color: #58A6FF; text-decoration: none;'>Ler notícia completa →</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Aguardando novas atualizações do feed de notícias...")
    except:
        st.error("Erro ao conectar com o servidor de notícias. Tente novamente em instantes.")

with col_info:
    st.subheader("📌 Avisos & Insights")
    st.info("💡 O mercado de FIIs mostra resiliência com a estabilidade da SELIC.")
    st.info("🔒 Seu patrimônio está 100% protegido em ativos de alta liquidez.")
