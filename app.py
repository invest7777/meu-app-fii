import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="XP Private | Dashboard", layout="wide", page_icon="🏦")

# Script para evitar erros de tradução que travam o app
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
    div[data-testid="stMetricValue"] { color: #C5A059 !important; font-weight: 800; font-size: 30px !important; }
    .stMetric label { color: #8B949E !important; text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- SUA CARTEIRA (VALOR INVESTIDO FIXO VS COTAÇÃO ATUAL) ---
# 'qtd': quantidade de cotas
# 'custo_total': quanto você pagou no total por aquelas cotas (R$ 29.773,28)
carteira_dados = {
    "MXRF11.SA": {"qtd": 204, "custo_total": 2001.24},
    "RECR11.SA": {"qtd": 26,  "custo_total": 2090.66},
    "VGHF11.SA": {"qtd": 340, "custo_total": 3009.60},
    "VISC11.SA": {"qtd": 18,  "custo_total": 2097.03},
    "XPML11.SA": {"qtd": 31,  "custo_total": 3448.44},
    "BTCI11.SA": {"qtd": 205, "custo_total": 2008.10},
    "HGLG11.SA": {"qtd": 31,  "custo_total": 5037.76},
    "KNCR11.SA": {"qtd": 98,  "custo_total": 10080.45}
}

@st.cache_data(ttl=60)
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
precos_mercado = buscar_cotacoes(list(carteira_dados.keys()))
detalhes = []
total_investido = 0
total_atual = 0

for ticker, info in carteira_dados.items():
    qtd = info['qtd']
    custo = info['custo_total']
    valor_atual = precos_mercado[ticker] * qtd
    
    total_investido += custo
    total_atual += valor_atual
    
    lucro_prejuizo = valor_atual - custo
    perc = (lucro_prejuizo / custo) * 100 if custo > 0 else 0
    
    detalhes.append({
        "ATIVO": ticker.replace(".SA", ""),
        "QTD": qtd,
        "CUSTO (R$)": custo,
        "ATUAL (R$)": valor_atual,
        "DIFERENÇA": lucro_prejuizo,
        "%": perc
    })

df = pd.DataFrame(detalhes)
diferenca_total = total_atual - total_investido
perc_total = (diferenca_total / total_investido) * 100 if total_investido > 0 else 0

# --- LAYOUT XP ---
st.markdown("<h2 style='color: #C5A059; margin-bottom: 0;'>XP PRIVATE</h2>", unsafe_allow_html=True)
st.caption(f"Consolidado de Ativos • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")

# Linha 1: Métricas de Comparação
c1, c2, c3 = st.columns(3)
c1.metric("VALOR TOTAL INVESTIDO", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("VALOR ATUAL (MERCADO)", f"R$ {total_atual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
          delta=f"{perc_total:.2f}%")
c3.metric("RESULTADO (DIFERENÇA)", f"R$ {diferenca_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
          delta=f"R$ {diferenca_total:,.2f}", delta_color="normal")

st.markdown("---")

# Gráfico e Tabela Detalhada
col_g, col_t = st.columns([1, 1.5])

with col_g:
    st.markdown("### Alocação Atual")
    fig = px.pie(df, values='ATUAL (R$)', names='ATIVO', hole=0.6,
                 color_discrete_sequence=px.colors.sequential.YlOrBr_r)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col_t:
    st.markdown("### Detalhamento da Diferença")
    # Formatação condicional para a tabela
    st.dataframe(df.style.format({
        "CUSTO (R$)": "R$ {:.2f}",
        "ATUAL (R$)": "R$ {:.2f}",
        "DIFERENÇA": "R$ {:.2f}",
        "%": "{:.2f}%"
    }), hide_index=True, use_container_width=True)

if st.button("🔄 Sincronizar com B3"):
    st.cache_data.clear()
    st.rerun()
