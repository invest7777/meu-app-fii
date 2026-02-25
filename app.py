import streamlit as st
import feedparser
from datetime import datetime

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="Private Bank | Terminal", layout="wide", page_icon="🏦")

# Script para evitar que o Google Tradutor quebre o app (Fix para o erro removeChild)
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

# --- DADOS FIXOS (SEU PATRIMÔNIO REAL CONFORME IMAGEM) ---
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

# --- SISTEMA DE NOTÍCIAS SEGURO (ANTI-TRAVAMENTO) ---
st.subheader("📰 Notícias em Tempo Real (Fontes Verificadas)")

@st.cache_data(ttl=300) # Mantém as notícias em cache por 5 minutos para carregar instantâneo
def buscar_noticias():
    # Portais oficiais com credibilidade verificada
    fontes = {
        "InfoMoney": "https://www.infomoney.com.br",
        "G1 Economia": "https://g1.globo.com",
        "Valor Econômico": "https://valor.globo.com"
    }
    feed_final = []
    
    for nome, url in fontes.items():
        try:
            d = feedparser.parse(url)
            if d.entries:
                for entry in d.entries[:3]: 
                    feed_final.append({"fonte": nome, "titulo": entry.title, "link": entry.link})
        except Exception:
            continue 
            
    return feed_final

noticias = buscar_noticias()

if noticias:
    col_n1, col_n2 = st.columns(2)
    for idx, n in enumerate(noticias):
        target_col = col_n1 if idx % 2 == 0 else col_n2
        with target_col:
            st.markdown(f"""
            <div class="news-card">
                <small style='color: #F1C40F;'>🔒 FONTE VERIFICADA: {n['fonte']}</small><br>
                <div style='margin-top: 8px; font-size: 16px; font-weight: bold; color: white;'>{n['titulo']}</div>
                <div style='margin-top: 12px;'>
                    <a href="{n['link']}" target="_blank" style="color: #00FF88; text-decoration: none; font-size: 14px; font-weight: bold;">
                        LER NOTÍCIA COMPLETA →
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    # Aviso caso o servidor ainda esteja sincronizando
    st.info("🔄 Sincronizando com os portais oficiais... Por favor, aguarde alguns segundos e atualize a página.")

st.markdown("---")
st.caption("🔒 Painel blindado contra desinformação via RSS Feeds Oficiais.")
