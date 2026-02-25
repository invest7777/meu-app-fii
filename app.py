import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="XP Private | Dashboard", layout="wide", page_icon="🏦")

# --- CSS CUSTOMIZADO (ESTILO XP INVESTIMENTOS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0E1117; }
    
    /* Estilização dos Cards de Métricas */
    div[data-testid="stMetric"] {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    div[data-testid="stMetricValue"] {
        color: #C5A059 !important; /* Dourado XP */
        font-weight: 800;
        font-size: 36px !important;
    }

    .stMetric label {
        color: #8B949E !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 13px;
    }

    /* Botão de Atualização */
    .stButton>button {
        background-color: #C5A059;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DA CARTEIRA (CONFORME SUA IMAGEM) ---
# Quantidades aproximadas para bater seu patrimônio real
carteira_cotas = {
    "MXRF11.SA": 204, "RECR11.SA": 26, "VGHF11.SA": 340, 
    "VISC11.SA": 18,  "XPML11.SA": 31, "BTCI11.SA": 205, 
    "HGLG11.SA": 31,  "KNCR11.SA": 98
}

@st.cache_data(ttl=300) # Atualiza a cada 5 minutos
def buscar_cotacoes(tickers):
    dados = {}
    for t in tickers:
        try:
            ticker_yf = yf.Ticker(t)
            # Pega preço atual da B3
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
        "QUANTIDADE": qtd,
        "COTAÇÃO ATUAL": precos[ticker],
        "POSIÇÃO (R$)": valor_mercado
    })

df = pd.DataFrame(detalhes)

# --- LAYOUT DO APP ---
# Cabeçalho com Logo Simulado
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.markdown("<h1 style='color: #C5A059; margin: 0;'>XP</h1>", unsafe_allow_html=True)
    st.caption("PRIVATE BANKING")

with col_titulo:
    st.title("Consolidado de Investimentos")
    st.write(f"🏦 **Status da Custódia** | {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")

# Linha de Destaque (Métricas)
c1, c2, c3 = st.columns(3)
c1.metric("Patrimônio Total Líquido", f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Proventos Estimados (Mês)", f"R$ {total_geral*0.0096:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c3.metric("Ativos sob Custódia", len(carteira_cotas))

st.markdown("---")

# Gráfico e Tabela
col_esq, col_dir = st.columns([1.5, 1])

with col_esq:
    st.markdown("### 📊 Alocação Estratégica por Ativo")
    fig = px.pie(df, values='POSIÇÃO (R$)', names='ATIVO', hole=0.6,
                 color_discrete_sequence=px.colors.sequential.YlOrBr_r) # Cores Douradas/Escuras
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col_dir:
    st.markdown("### 📋 Extrato de Posição")
    st.dataframe(df.style.format({
        "COTAÇÃO ATUAL": "R$ {:.2f}",
        "POSIÇÃO (R$)": "R$ {:.2f}"
    }), hide_index=True, use_container_width=True)
    
    if st.button("🔄 Sincronizar com B3 agora"):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")
st.caption("⚠️ Dados em tempo real fornecidos por Yahoo Finance. A atualização pode ter até 15 min de atraso conforme normas da B3.")
