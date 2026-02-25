import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE XP ---
st.set_page_config(page_title="XP Private | Painel de Controle", layout="wide", page_icon="🏦")

# Bloqueia tradutor do navegador que causa erro de sincronização
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# --- ESTILO XP INVESTIMENTOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 20px;
    }
    div[data-testid="stMetricValue"] { color: #C5A059 !important; font-weight: 800; font-size: 30px !important; }
    .stMetric label { color: #8B949E !important; text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL PARA EDIÇÃO DE ATIVOS ---
st.sidebar.header("📝 Ajustar Carteira")
st.sidebar.caption("Altere as quantidades para bater com o Nubank")

tickers = ["MXRF11.SA", "RECR11.SA", "VGHF11.SA", "VISC11.SA", "XPML11.SA", "BTCI11.SA", "HGLG11.SA", "KNCR11.SA"]

# Valores iniciais baseados na sua imagem anterior
valores_padrao = {
    "MXRF11.SA": {"qtd": 204, "pm": 10.15}, "RECR11.SA": {"qtd": 26, "pm": 85.20},
    "VGHF11.SA": {"qtd": 340, "pm": 9.25}, "VISC11.SA": {"qtd": 18, "pm": 115.50},
    "XPML11.SA": {"qtd": 31, "pm": 112.40}, "BTCI11.SA": {"qtd": 205, "pm": 10.05},
    "HGLG11.SA": {"qtd": 31, "pm": 165.20}, "KNCR11.SA": {"qtd": 98, "pm": 102.50}
}

carteira_usuario = {}
for t in tickers:
    with st.sidebar.expander(f"🔹 {t.replace('.SA', '')}"):
        qtd = st.number_input(f"Quantidade", value=valores_padrao[t]["qtd"], step=1, key=f"q_{t}")
        pm = st.number_input(f"Preço Médio", value=valores_padrao[t]["pm"], step=0.01, key=f"p_{t}")
        carteira_usuario[t] = {"qtd": qtd, "pm": pm}

@st.cache_data(ttl=60)
def buscar_cotacoes(lista_tickers):
    dados = {}
    for t in lista_tickers:
        try:
            ticker_yf = yf.Ticker(t)
            dados[t] = ticker_yf.fast_info['last_price']
        except:
            dados[t] = 0.0
    return dados

# --- CÁLCULOS ---
precos_mercado = buscar_cotacoes(tickers)
detalhes = []
total_investido = 0
total_atual = 0

for t, info in carteira_usuario.items():
    investido = info["qtd"] * info["pm"]
    atual = info["qtd"] * precos_mercado[t]
    total_investido += investido
    total_atual += atual
    detalhes.append({
        "ATIVO": t.replace(".SA", ""),
        "QTD": info["qtd"],
        "VALOR INVESTIDO": investido,
        "VALOR ATUAL": atual,
        "DIFERENÇA": atual - investido
    })

df = pd.DataFrame(detalhes)

# --- DASHBOARD ---
st.markdown("<h2 style='color: #C5A059; margin-bottom: 0;'>XP PRIVATE</h2>", unsafe_allow_html=True)
st.caption(f"Sincronizado com B3 em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")

c1, c2, c3 = st.columns(3)
c1.metric("TOTAL INVESTIDO", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("PATRIMÔNIO ATUAL (B3)", f"R$ {total_atual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
          delta=f"{((total_atual/total_investido)-1)*100:.2f}%" if total_investido > 0 else "0%")
c3.metric("RESULTADO (R$)", f"R$ {(total_atual - total_investido):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

col_g, col_t = st.columns([1, 1.5])
with col_g:
    st.plotly_chart(px.pie(df, values='VALOR ATUAL', names='ATIVO', hole=0.6, 
                           color_discrete_sequence=px.colors.sequential.YlOrBr_r).update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False), use_container_width=True)

with col_t:
    st.dataframe(df.style.format({"VALOR INVESTIDO": "R$ {:.2f}", "VALOR ATUAL": "R$ {:.2f}", "DIFERENÇA": "R$ {:.2f}"}), use_container_width=True, hide_index=True)

if st.button("🔄 Forçar Atualização B3"):
    st.cache_data.clear()
    st.rerun()
