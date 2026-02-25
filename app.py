import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO PREMIUM ---
st.set_page_config(page_title="Private Bank | Painel Global", layout="wide", page_icon="🏦")

# CSS Avançado: Cores Profissionais e Efeitos de Card
st.markdown("""
    <style>
    .main { background-color: #0B0E11; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stInfo { background-color: #161B22; border: 1px solid #30363D; border-left: 5px solid #F1C40F; border-radius: 10px; }
    h1, h2, h3 { color: #FFFFFF; font-family: 'Poppins', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS FIXOS (SEU PATRIMÔNIO) ---
patrimonio = 29773.28
divs_est = 285.82

# --- CABEÇALHO COM ÍCONES ---
st.title("🏛️ Banco Privado - Painel Global")
st.caption(f"🔄 Sincronizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- DASHBOARD PRINCIPAL ---
c1, c2, c3 = st.columns(3)
c1.metric("💰 Patrimônio Total", f"R$ {patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("📊 Classe Principal", "FIIs (100%)")
c3.metric("💸 Dividendos Est. (Mês)", f"R$ {divs_est:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- RADAR DE MERCADO (COM SÍMBOLOS) ---
st.subheader("⚡ Radar de Mercado (Cripto & Índices)")
col_m = st.columns(4)

monitor = {"BTC-USD": "₿ Bitcoin", "ETH-USD": "Ξ Ethereum", "^BVSP": "🇧🇷 Ibovespa", "USDBRL=X": "💵 Dólar"}

for i, (ticker, nome) in enumerate(monitor.items()):
    try:
        # Busca dados e garante atualização do yfinance
        stock = yf.Ticker(ticker)
        info = stock.fast_info
        preco = info['last_price']
        var = ((preco / info['previous_close']) - 1) * 100
        simbolo = "US$ " if "USD" in ticker else "R$ " if "BRL" in ticker else ""
        col_m[i].metric(nome, f"{simbolo}{preco:,.2f}", f"{var:.2f}%")
    except: pass

st.markdown("---")

# --- CORREÇÃO DAS NOTÍCIAS (SOLUÇÃO REAL-TIME) ---
st.subheader("📰 Notícias Globais em Tempo Real")
try:
    # A dica aqui é usar o índice geral para buscar notícias mundiais
    news_feed = yf.Ticker("^BVSP").news[:6] 
    if news_feed:
        # Layout de 2 colunas para as notícias
        n_col1, n_col2 = st.columns(2)
        for i, n in enumerate(news_feed):
            target_col = n_col1 if i % 2 == 0 else n_col2
            with target_col:
                st.info(f"**{n['publisher']}** • _{datetime.fromtimestamp(n['providerPublishTime']).strftime('%H:%M')}_\n\n"
                        f"**{n['title']}**\n\n"
                        f"[Clique para ler na íntegra]({n['link']})")
    else:
        st.warning("⚠️ O Yahoo Finance limitou o acesso às notícias. Tente atualizar em instantes.")
except Exception as e:
    st.error(f"Erro ao carregar feed: {e}")
