import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="Private Bank | Dashboard", layout="wide", page_icon="🏦")

# Script para evitar que o Google Tradutor quebre o app
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# --- CSS PREMIUM (BLACK & NEON GOLD) ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 25px;
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 32px !important; font-weight: bold; }
    
    /* ESTILO DOS CARDS DE NOTÍCIAS */
    .news-card {
        background-color: #161B22;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #F1C40F;
        margin-bottom: 15px;
        border: 1px solid #30363D;
        transition: 0.3s;
    }
    .news-card:hover { border-color: #F1C40F; transform: translateY(-3px); }
    .news-tag { color: #F1C40F; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .news-title { margin-top: 8px; font-size: 17px; font-weight: bold; color: #FFFFFF; line-height: 1.4; }
    .news-link { margin-top: 15px; display: inline-block; color: #00FF88; text-decoration: none; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- PATRIMÔNIO REAL (FIXO: R$ 29.773,28) ---
patrimonio = 29773.28
divs_estimados = patrimonio * 0.0096 

# --- CABEÇALHO ---
st.title("🏛️ Banco Privado - Terminal de Investimentos")
st.caption(f"🚀 Status: On-line • Conectado à B3 & World Stream • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

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

# --- LINHA 3: NOTÍCIAS (SISTEMA DE BUSCA BLINDADO) ---
st.subheader("📰 Notícias do Mercado (World Stream)")

def carregar_noticias_reais():
    # Tenta buscar notícias de fontes globais mais estáveis
    fontes = ["^BVSP", "BTC-USD", "AAPL", "MSFT"]
    feed_final = []
    
    for fonte in fontes:
        try:
            raw_news = yf.Ticker(fonte).news
            for item in raw_news:
                # SÓ ADICIONA SE TIVER TÍTULO E LINK REAIS
                if item.get('title') and item.get('link') and item['title'] != "Sem título":
                    if item['title'] not in [n['title'] for n in feed_final]: # Evita duplicados
                        feed_final.append(item)
            if len(feed_final) >= 8: break
        except: continue
    return feed_final[:8]

noticias = carregar_noticias_reais()

if noticias:
    col_n1, col_n2 = st.columns(2)
    for idx, n in enumerate(noticias):
        target_col = col_n1 if idx % 2 == 0 else col_n2
        with target_col:
            publisher = n.get('publisher', 'MERCADO')
            st.markdown(f"""
            <div class="news-card">
                <span class="news-tag">{publisher}</span>
                <div class="news-title">{n['title']}</div>
                <a class="news-link" href="{n['link']}" target="_blank">LER RELATÓRIO COMPLETO +</a>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("🔄 Sincronizando notícias com o servidor global... Tente atualizar em instantes.")

st.markdown("---")
st.caption("⚠️ Dados fornecidos por Yahoo Finance API. Dashboard para fins de visualização pessoal.")
