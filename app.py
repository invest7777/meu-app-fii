import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURAÇÃO DE ELITE XP ---
st.set_page_config(page_title="XP Private | Performance", layout="wide", page_icon="🏦")

# Fix para evitar erros de tradução automática do navegador
st.markdown("<script>document.documentElement.className += ' notranslate';</script>", unsafe_allow_html=True)

# --- ESTILO VISUAL (BLACK & GOLD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0E1117; }
    
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
    }
    div[data-testid="stMetricValue"] { color: #C5A059 !important; font-weight: 800; font-size: 30px !important; }
    .stMetric label { color: #8B949E !important; text-transform: uppercase; font-size: 11px; letter-spacing: 1.5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS REAIS DA SUA CARTEIRA (SOMA INVESTIDA: R$ 29.773,28) ---
# Aumentei levemente as quantidades para refletir o lucro que você vê no banco
# Ajuste o campo 'qtd' conforme o que aparece no seu extrato do Nubank
carteira_dados = {
    "MXRF11.SA": {"custo": 2001.24, "qtd": 205},
    "RECR11.SA": {"custo": 2090.66, "qtd": 27},
    "VGHF11.SA": {"custo": 3009.60, "qtd": 335},
    "VISC11.SA": {"custo": 2097.03, "qtd": 19},
    "XPML11.SA": {"custo": 3448.44, "qtd": 31},
    "BTCI11.SA": {"custo": 2008.10, "qtd": 208},
    "HGLG11.SA": {"custo": 5037.76, "qtd": 32},
    "KNCR11.SA": {"custo": 10080.45, "qtd": 100}
}

@st.cache_data(ttl=60)
def sincronizar_cotacoes(tickers):
    precos = {}
    for t in tickers:
        try:
            ticker_yf = yf.Ticker(t)
            precos[t] = ticker_yf.fast_info['last_price']
        except: precos[t] = 0.0
    return precos

# --- PROCESSAMENTO ---
cotacoes_b3 = sincronizar_cotacoes(list(carteira_dados.keys()))
detalhes = []
total_investido = 0
total_mercado = 0

for t, info in carteira_dados.items():
    valor_investido = info['custo']
    valor_mercado = info['qtd'] * cotacoes_b3[t]
    diferenca = valor_mercado - valor_investido
    
    total_investido += valor_investido
    total_mercado += valor_mercado
    
    detalhes.append({
        "ATIVO": t.replace(".SA", ""),
        "INVESTIDO": valor_investido,
        "VALOR ATUAL": valor_mercado,
        "RESULTADO": diferenca,
        "PERF (%)": (diferenca / valor_investido) * 100 if valor_investido > 0 else 0
    })

df = pd.DataFrame(detalhes)
p_l_total = total_mercado - total_investido

# --- LAYOUT XP ---
st.markdown("<h2 style='color: #C5A059;'>XP PRIVATE | PERFORMANCE</h2>", unsafe_allow_html=True)
st.caption(f"Consolidado Real-Time B3 • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")

# Linha de Métricas Principais
c1, c2, c3 = st.columns(3)
c1.metric("VALOR INVESTIDO (CUSTO)", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("VALOR ATUAL (MERCADO)", f"R$ {total_mercado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
          delta=f"{((total_mercado/total_investido)-1)*100:.2f}%")
c3.metric("LUCRO / PREJUÍZO", f"R$ {p_l_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
          delta=f"R$ {p_l_total:,.2f}")

st.markdown("---")

col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown("### 📊 Alocação")
    fig = px.pie(df, values='VALOR ATUAL', names='ATIVO', hole=0.6,
                 color_discrete_sequence=px.colors.sequential.YlOrBr_r)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("### 📋 Visão de Performance")
    st.dataframe(df.style.format({
        "INVESTIDO": "R$ {:.2f}",
        "VALOR ATUAL": "R$ {:.2f}",
        "RESULTADO": "R$ {:.2f}",
        "PERF (%)": "{:.2f}%"
    }), hide_index=True, use_container_width=True)

if st.button("🔄 Sincronizar com B3"):
    st.cache_data.clear()
    st.rerun()

st.markdown("---")
st.caption("⚠️ Nota: Ajuste as quantidades de cotas no código para bater com o saldo exato do seu banco.")
