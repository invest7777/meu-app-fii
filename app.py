import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Private Bank Dashboard", layout="wide")

# CSS para customizar as métricas (Deixa o visual mais "limpo")
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 32px; color: #2ecc71; }
    .stPlotlyChart { border-radius: 15px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DA SUA CARTEIRA (R$ 29.773,28) ---
carteira = {
    "MXRF11": 2001.24, "RECR11": 2090.66, "VGHF11": 3009.60,
    "VISC11": 2097.03, "XPML11": 3448.44, "BTCI11": 2008.10,
    "HGLG11": 5037.76, "KNCR11": 10080.45
}

# --- CÁLCULOS ---
total = sum(carteira.values())
dividendos_mes = total * 0.0096 # Baseado no seu 0.96% da imagem

# --- CABEÇALHO ---
st.title("🏛 Minha Carteira Profissional")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- RESUMO DE TOPO (KPIs) ---
c1, c2, c3 = st.columns(3)
c1.metric("Patrimônio Total", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Dividendos Estimados", f"R$ {dividendos_mes:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c3.metric("Yield Médio", "0.96%", delta="0.02% (mês)")

st.markdown("---")

# --- GRÁFICOS INTERATIVOS ---
col_graf1, col_graf2 = st.columns([1.2, 1])

with col_graf1:
    st.markdown("### 📊 Alocação Estratégica")
    df = pd.DataFrame(list(carteira.items()), columns=['FII', 'Valor'])
    # Gráfico Donut (mais moderno que barras para alocação)
    fig = px.pie(df, values='Valor', names='FII', hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Greens_r)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col_graf2:
    st.markdown("### 📰 Notícias do Mundo")
    try:
        # Busca notícias reais via Yahoo Finance
        noticias = yf.Ticker("^BVSP").news[:4]
        for n in noticias:
            st.info(f"**{n['title']}**")
            st.caption(f"[Clique aqui para ler]({n['link']})")
    except:
        st.write("Sem notícias no momento.")

# --- TABELA DE CONTROLE ---
with st.expander("👁 Ver Detalhamento dos Ativos"):
    df_tabela = pd.DataFrame(list(carteira.items()), columns=['Ticker', 'Saldo Atual'])
    st.table(df_tabela.style.format({'Saldo Atual': 'R$ {:.2f}'}))
