import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="XP Private | Dashboard", layout="wide", page_icon="🏦")

# Script para evitar erros de tradução
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# --- ESTILO XP INVESTIMENTOS (BLACK & GOLD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0E1117; }
    
    /* Estilo dos Cards */
    div[data-testid="stMetric"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    div[data-testid="stMetricValue"] { color: #C5A059 !important; font-weight: 800; font-size: 32px !important; }
    .stMetric label { color: #8B949E !important; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- SUA CARTEIRA REAL (Ajuste as Qtds aqui se necessário) ---
# Se o valor no app está baixo, é porque as quantidades abaixo estão menores que as suas reais
carteira_cotas = {
    "MXRF11.SA": 204, "RECR11.SA": 26, "VGHF11.SA": 340, 
    "VISC11.SA": 18,  "XPML11.SA": 31, "BTCI11.SA": 205, 
    "HGLG11.SA": 31,  "KNCR11.SA": 98
}

@st.cache_data(ttl=60) # Atualiza cotação a cada 1 minuto
def buscar_cotacoes(tickers):
    dados = {}
    for t in tickers:
        try:
            ticker_yf = yf.Ticker(t)
            dados[t] = ticker_yf.fast_info['last_price']
        except:
            dados[t] = 0.0
    return dados

# --- PROCESSAMENTO ---
precos = buscar_cotacoes(list(carteira_cotas.keys()))
detalhes = []
total_geral = 0

for ticker, qtd in carteira_cotas.items():
    valor_mercado = precos[ticker] * qtd
    total_geral += valor_mercado
    detalhes.append({
        "ATIVO": ticker.replace(".SA", ""),
        "QTD": qtd,
        "PREÇO": precos[ticker],
        "SUBTOTAL": valor_mercado
    })

df = pd.DataFrame(detalhes)

# --- LAYOUT XP ---
st.markdown("<h2 style='color: #C5A059; margin-bottom: 0;'>XP PRIVATE</h2>", unsafe_allow_html=True)
st.caption(f"Cotações B3 em tempo real • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")

# Métricas Principais
c1, c2, c3 = st.columns(3)
c1.metric("PATRIMÔNIO TOTAL LÍQUIDO", f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("PROVENTOS ESTIMADOS (MÊS)", f"R$ {total_geral*0.0096:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c3.metric("ATIVOS SOB CUSTÓDIA", len(carteira_cotas))

st.markdown("---")

# Gráfico e Tabela
col_g, col_t = st.columns([1.2, 1])

with col_g:
    st.markdown("### Alocação de Ativos")
    fig = px.pie(df, values='SUBTOTAL', names='ATIVO', hole=0.6,
                 color_discrete_sequence=px.colors.sequential.YlOrBr_r)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col_t:
    st.markdown("### Detalhamento")
    st.dataframe(df.style.format({"PREÇO": "R$ {:.2f}", "SUBTOTAL": "R$ {:.2f}"}), hide_index=True)
    
    if st.button("🔄 Sincronizar com B3"):
        st.cache_data.clear()
        st.rerun()
