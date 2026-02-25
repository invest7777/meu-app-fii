import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="Private Bank | Terminal", layout="wide", page_icon="🏦")

# Script anti-erro de interface (desativa tradutor do navegador)
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# --- CSS PREMIUM (MODO DARK DEEP & NEON GOLD) ---
st.markdown("""
    <style>
    .main { background-color: #0B0E11; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 34px !important; font-weight: 900; }
    
    /* CARDS DE NOTÍCIAS ESTILO TERMINAL */
    .news-card {
        background-color: #161B22;
        padding: 22px;
        border-radius: 12px;
        border-left: 6px solid #F1C40F;
        margin-bottom: 18px;
        border-top: 1px solid #30363D;
        border-right: 1px solid #30363D;
        border-bottom: 1px solid #30363D;
        transition: 0.4s;
    }
    .news-card:hover { border-color: #00FF88; transform: scale(1.01); background-color: #1C2128; }
    .news-tag { color: #F1C40F; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    .news-title { margin-top: 10px; font-size: 18px; font-weight: bold; color: #FFFFFF; line-height: 1.5; }
    .news-link { margin-top: 15px; display: inline-block; color: #00FF88; text-decoration: none; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- PATRIMÔNIO REAL (TRAVADO EM R$ 29.773,28) ---
patrimonio = 29773.28
divs_estimados = patrimonio * 0.0096 

# --- HEADER PRINCIPAL ---
st.title("🏛️ Banco Privado - Terminal de Investimentos")
st.caption(f"🚀 Global Market Connection • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- LINHA 1: MÉTRICAS DE PATRIMÔNIO ---
c1, c2, c3 = st.columns(3)
c1.metric("💰 Patrimônio Total", f"R$ {patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("📊 Classe Principal", "FIIs (100%)")
c3.metric("💸 Proventos Est. (Mês)", f"R$ {divs_estimados:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- LINHA 2: RADAR DE MERCADO EM TEMPO REAL ---
st.subheader("⚡ Radar de Mercado em Tempo Real")
m1, m2, m3, m4 = st.columns(4)
monitor = {"BTC-USD": "₿ Bitcoin", "ETH-USD": "Ξ Ethereum", "^BVSP": "📈 Ibovespa", "USDBRL=X": "💵 Dólar"}

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

# --- LINHA 3: SISTEMA DE NOTÍCIAS MULTI-FONTE ---
st.subheader("📰 Notícias do Mercado (World Stream)")

def carregar_noticias_blindadas():
    # Tenta várias fontes caso uma esteja bloqueada
    fontes = ["^BVSP", "BTC-USD", "GC=F", "CL=F"] # Ibov, Bitcoin, Ouro, Petróleo
    noticias_validadas = []
    
    for f in fontes:
        try:
            feed = yf.Ticker(f).news
            for n in feed:
                # Valida se a notícia é real e não está duplicada
                if n.get('title') and n.get('link') and n['title'] not in [x['title'] for x in noticias_validadas]:
                    noticias_validadas.append(n)
            if len(noticias_validadas) >= 10: break
        except: continue
    return noticias_validadas[:10]

noticias = carregar_noticias_blindadas()

if noticias:
    col_n1, col_n2 = st.columns(2)
    for idx, n in enumerate(noticias):
        target_col = col_n1 if idx % 2 == 0 else col_n2
        with target_col:
            publisher = n.get('publisher', 'INSIGHTS')
            st.markdown(f"""
            <div class="news-card">
                <span class="news-tag">{publisher}</span>
                <div class="news-title">{n['title']}</div>
                <a class="news-link" href="{n['link']}" target="_blank">ACESSAR RELATÓRIO COMPLETO →</a>
            </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ Sincronizando com servidores globais de notícias... Por favor, aguarde 30 segundos e atualize a página.")

st.markdown("---")
st.caption("A Dados fornecidos por Yahoo Finance API. Painel exclusivo para visualização pessoal.")
