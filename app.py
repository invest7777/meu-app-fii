import streamlit as st
import feedparser
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="Private Bank | Terminal", layout="wide", page_icon="🏦")

# Script para evitar que o navegador quebre o layout (Fix para Google Tradutor)
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# --- CSS PREMIUM (BLACK & GOLD) ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 12px; padding: 25px;
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 32px !important; font-weight: 800; }
    .news-card {
        background-color: #161B22; padding: 20px; border-radius: 12px;
        border-left: 5px solid #F1C40F; margin-bottom: 15px; border: 1px solid #30363D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS FIXOS DO SEU PATRIMÔNIO (R$ 29.773,28) ---
patrimonio = 29773.28
divs_est = 285.82

# --- CABEÇALHO ---
st.title("🏛️ Banco Privado - Terminal de Notícias Verificadas")
st.caption(f"🛡️ Fontes Seguras Selecionadas • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- DASHBOARD DE MÉTRICAS ---
c1, c2, c3 = st.columns(3)
c1.metric("💰 Patrimônio Total", f"R$ {patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("📊 Classe Principal", "FIIs (100%)")
c3.metric("💸 Proventos Est. (Mês)", f"R$ {divs_est:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- SISTEMA DE NOTÍCIAS BLINDADO (FONTES OFICIAIS) ---
st.subheader("📰 Notícias em Tempo Real (Fontes Verificadas)")

def buscar_noticias():
    # Fontes RSS de portais de alta credibilidade
    fontes = {
        "InfoMoney": "https://www.infomoney.com.br",
        "G1 Economia": "https://g1.globo.com",
        "Valor Econômico": "https://valor.globo.com"
    }
    feed_final = []
    for nome, url in fontes.items():
        try:
            d = feedparser.parse(url)
            for entry in d.entries[:3]: # Pega as 3 mais recentes de cada
                feed_final.append({"fonte": nome, "titulo": entry.title, "link": entry.link})
        except: continue
    return feed_final

noticias = buscar_noticias()

if noticias:
    col_n1, col_n2 = st.columns(2)
    for idx, n in enumerate(noticias):
        target_col = col_n1 if idx % 2 == 0 else col_n2
        with target_col:
            st.markdown(f"""
            <div class="news-card">
                <small style='color: #F1C40F;'>🔒 FONTE: {n['fonte']}</small><br>
                <div style='margin-top: 8px; font-size: 16px; font-weight: bold; color: white;'>{n['titulo']}</div>
                <div style='margin-top: 12px;'>
                    <a href="{n['link']}" target="_blank" style="color: #00FF88; text-decoration: none; font-size: 14px;">
                        LER NOTÍCIA COMPLETA →
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ Erro de conexão com os portais. Por favor, reinicie o app no painel do Streamlit.")

st.markdown("---")
st.caption("🔒 Este painel utiliza apenas protocolos oficiais de notícias para evitar desinformação.")
