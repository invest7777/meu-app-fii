import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE & FIX DE ERRO ---
st.set_page_config(page_title="Private Bank | Dashboard", layout="wide", page_icon="🏦")

# Script para evitar que o Google Tradutor quebre o app
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# --- CSS PROFISSIONAL ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 25px;
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 32px !important; font-weight: bold; }
    .news-card {
        background-color: #161B22;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #F1C40F;
        margin-bottom: 10px;
        border: 1px solid #30363D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PATRIMÔNIO REAL (FIXO: R$ 29.773,28) ---
patrimonio = 29773.28
divs_estimados = patrimonio * 0.0096 

# --- CABEÇALHO ---
st.title("🏛️ Banco Privado - Terminal de Investimentos")
st.caption(f"🚀 Status: On-line • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

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

# --- LINHA 3: NOTÍCIAS (SISTEMA DE SEGURANÇA MULTI-FONTE) ---
st.subheader("📰 Notícias do Mercado (World Stream)")

def exibir_noticias():
    # Tenta buscar notícias de diferentes fontes para garantir que o painel não fique vazio
    tickers_para_noticias = ["^BVSP", "BTC-USD", "AAPL"]
    feed = []
    
    for t in tickers_para_noticias:
        try:
            temp_feed = yf.Ticker(t).news
            if temp_feed:
                feed.extend(temp_feed)
            if len(feed) >= 6: break # Para quando tiver notícias suficientes
        except: continue

    if feed:
        col_n1, col_n2 = st.columns(2)
        for idx, n in enumerate(feed[:8]): # Mostra as 8 mais recentes
            target_col = col_n1 if idx % 2 == 0 else col_n2
            with target_col:
                st.markdown(f"""
                <div class="news-card">
                    <small style='color: #F1C40F;'>{n.get('publisher', 'Mercado')}</small><br>
                    <div style='margin-top: 5px; font-size: 15px; font-weight: bold; color: white;'>{n.get('title', 'Sem título')}</div>
                    <div style='margin-top: 10px;'>
                        <a href="{n.get('link', '#')}" target="_blank" style="color: #00FF88; text-decoration: none; font-size: 13px;">
                            LER RELATÓRIO COMPLETO →
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ O servidor de notícias está instável no momento. Tente atualizar a página.")

exibir_noticias()
