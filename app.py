import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="Private Bank | Terminal Seguro", layout="wide", page_icon="🏦")

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
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 34px !important; font-weight: 900; }
    .news-card {
        background-color: #161B22;
        padding: 22px;
        border-radius: 12px;
        border-left: 6px solid #F1C40F;
        margin-bottom: 18px;
        border: 1px solid #30363D;
    }
    .news-tag { color: #F1C40F; font-size: 11px; font-weight: 800; text-transform: uppercase; }
    .news-title { margin-top: 10px; font-size: 18px; font-weight: bold; color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# --- PATRIMÔNIO REAL (TRAVADO EM R$ 29.773,28) ---
patrimonio = 29773.28
divs_estimados = patrimonio * 0.0096 

# --- HEADER PRINCIPAL ---
st.title("🏛️ Banco Privado - Terminal de Notícias Verificadas")
st.caption(f"🛡️ Fontes Seguras Selecionadas • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- LINHA 1: MÉTRICAS ---
c1, c2, c3 = st.columns(3)
c1.metric("💰 Patrimônio Total", f"R$ {patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("📊 Classe Principal", "FIIs (100%)")
c3.metric("💸 Proventos Est. (Mês)", f"R$ {divs_estimados:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# --- SISTEMA DE NOTÍCIAS BLINDADO (RSS FEED) ---
st.subheader("📰 Notícias em Tempo Real (Fontes Oficiais)")

def buscar_noticias_seguras():
    # LISTA DE FONTES SEGURAS (ADICIONE OU REMOVA AQUI)
    fontes_rss = {
        "Reuters Finance": "https://www.reutersagency.com",
        "InfoMoney": "https://www.infomoney.com.br",
        "G1 Economia": "https://g1.globo.com"
    }
    
    noticias_validadas = []
    
    for nome_fonte, url in fontes_rss.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]: # Pega as 4 mais recentes de cada
                noticias_validadas.append({
                    "fonte": nome_fonte,
                    "titulo": entry.title,
                    "link": entry.link,
                    "data": entry.get('published', 'Agora')
                })
        except: continue
        
    return noticias_validadas

noticias = buscar_noticias_seguras()

if noticias:
    col_n1, col_n2 = st.columns(2)
    for idx, n in enumerate(noticias):
        target_col = col_n1 if idx % 2 == 0 else col_n2
        with target_col:
            st.markdown(f"""
            <div class="news-card">
                <span class="news-tag">🔒 FONTE: {n['fonte']}</span>
                <div class="news-title">{n['titulo']}</div>
                <a href="{n['link']}" target="_blank" style="color: #00FF88; text-decoration: none; font-weight: bold; font-size: 14px;">
                    VERIFICAR NOTÍCIA COMPLETA →
                </a>
            </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ Sincronizando com as fontes oficiais... Por favor, aguarde e atualize a página.")

st.markdown("---")
st.caption("🔒 Este painel utiliza apenas protocolos oficiais de notícias para evitar desinformação.")
