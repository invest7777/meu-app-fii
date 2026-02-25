import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Meu Portfólio VIP", layout="wide", page_icon="💰")

# CSS para visual de banco (Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 20px;
    }
    div[data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 32px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SUA CARTEIRA ATUALIZADA ---
# Coloque a QUANTIDADE exata de cotas que você possui
carteira_cotas = {
    "MXRF11.SA": 204, "RECR11.SA": 26, "VGHF11.SA": 340, 
    "VISC11.SA": 18,  "XPML11.SA": 31, "BTCI11.SA": 205, 
    "HGLG11.SA": 31,  "KNCR11.SA": 98
}

@st.cache_data(ttl=60) # Atualiza os preços a cada 60 segundos
def buscar_dados_mercado(tickers):
    dados = {}
    for ticker in tickers:
        try:
            obj = yf.Ticker(ticker)
            # Pega o último preço de fechamento/atual
            preco = obj.fast_info['last_price']
            dados[ticker] = preco
        except:
            dados[ticker] = 0
    return dados

# --- PROCESSAMENTO DOS DADOS ---
precos_atuais = buscar_dados_mercado(list(carteira_cotas.keys()))
detalhes = []
total_patrimonio = 0

for ticker, qtd in carteira_cotas.items():
    preco = precos_atuais[ticker]
    subtotal = preco * qtd
    total_patrimonio += subtotal
    detalhes.append({
        "Ativo": ticker.replace(".SA", ""),
        "Qtd": qtd,
        "Preço Atual": preco,
        "Total (R$)": subtotal
    })

df_portfolio = pd.DataFrame(detalhes)

# --- EXIBIÇÃO NO APP ---
st.title("🏛️ Portfólio de Investimentos - Real Time")
st.caption(f"Última atualização do mercado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Métricas Principais
col1, col2 = st.columns(2)
col1.metric("Patrimônio Total Atualizado", f"R$ {total_patrimonio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Total de Ativos", len(carteira_cotas))

st.markdown("---")

# Gráfico de Alocação
st.subheader("📊 Distribuição de Patrimônio (Valor de Mercado)")
fig = px.pie(df_portfolio, values='Total (R$)', names='Ativo', hole=0.5,
             color_discrete_sequence=px.colors.sequential.Greens_r)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
st.plotly_chart(fig, use_container_width=True)

# Tabela Detalhada
st.subheader("📋 Detalhamento da Carteira")
st.dataframe(df_portfolio.style.format({
    "Preço Atual": "R$ {:.2f}",
    "Total (R$)": "R$ {:.2f}"
}), use_container_width=True)

# Botão de Atualização Manual
if st.button("🔄 Forçar Atualização de Preços"):
    st.cache_data.clear()
    st.rerun()
