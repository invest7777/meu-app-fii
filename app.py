import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="Private Bank | Dashboard", layout="wide", page_icon="🏦")

# Script para evitar que o Google Tradutor quebre o app
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# CSS PROFISSIONAL: Dark Mode, Neon & Gold
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 32px !important; font-weight: 800; }
    .stMetric label { color: #8B949E !important; font-size: 16px; font-weight: 600; }
    .news-card {
        background-color: #161B22;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #F1C40F;
        margin-bottom: 15px;
        border: 1px solid #30363D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PATRIMÔNIO REAL (FIXO: R$ 29.773,28) ---
patrimonio = 29773.28
divs_estimados = patrimonio * 0.0096 

# --- CABEÇALHO ---
st.title("🏛️ Banco Privado - Terminal de Investimentos")
st.caption(f"🚀 Conectado à B3 & Mercado Global • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- LINHA 1: MÉTRICAS ---
c1, c2, c3 = st.columns(3)
c1.metric("💰 Patrimônio Total", f"R$ {patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("📊 Classe Principal", "FIIs (100%)")
c3.metric("💸 Proventos Est. (Mês)", f"R$ {divs_estimados:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- LINHA 2: RADAR DE MERCADO ---
st.subheader("⚡ Radar de Mercado em Tempo Real")
m1, m2, m3, m4 = st.columns(4)

monitor = {"BTC-USD": "₿ Bitcoin", "ETH-USD": "Ξ Ethereum", "^BVSP": "📉 Ibovespa", "USDBRL=X": "💵 Dólar"}

for i, (ticker, nome) in enumerate(monitor.items()):
    try:
        data = yf.Ticker(ticker).fast_info
        preco = data['last_price']
        var = ((preco / data['previous_close']) - 1) * 100
        simbolo = "US$ " if "USD" in ticker else "R$ " if "BRL" in ticker else ""
        cols = [m1, m2, m3, m4]
        cols[i].metric(nome, f"{simbolo}{preco:,.2f}", f"{var:.2f}%")
    except: pass

st.markdown("---")

# --- LINHA 3: NOTÍCIAS ---
st.subheader("📰 Notícias do Mercado (World Stream)")
try:
    feed = yf.Ticker("^BVSP").news[:6]
    if feed:
        col_n1, col_n2 = st.columns(2)
        for idx, n in enumerate(feed):
            target_col = col_n1 if idx % 2 == 0 else col_n2
            with target_col:
                st.markdown(f"""
                <div class="news-card">
                    <small style='color: #F1C40F;'>{n['publisher']}</small><br>
                    <div style='margin-top: 8px; font-size: 16px; font-weight: bold; color: white;'>{n['title']}</div>
                    <div style='margin-top: 12px;'>
                        <a href="{n['link']}" target="_blank" style="color: #00FF88; text-decoration: none; font-size: 14px;">
                            LER NOTÍCIA COMPLETA →
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
except:
    st.info("🔄 Sincronizando notícias...")
