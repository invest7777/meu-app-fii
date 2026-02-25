import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="XP Private | Intelligence", layout="wide", page_icon="🏦")

# CSS PREMIUM: Cores Profissionais e Efeitos de Card
st.markdown("""
    <style>
    .main { background-color: #0B0E11; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-radius: 15px; padding: 20px;
    }
    div[data-testid="stMetricValue"] { color: #C5A059 !important; font-weight: 800; }
    .stDataFrame { border: 1px solid #30363D; border-radius: 10px; }
    .opportunity-card {
        background-color: #1E2329; border-left: 5px solid #00FF88;
        padding: 15px; border-radius: 10px; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS (SUA CARTEIRA REAL) ---
# Adicione o seu Preço Médio (PM) para o cálculo do "Total Investido" ficar correto
carteira_dados = {
    "MXRF11.SA": {"qtd": 204, "pm": 10.15}, 
    "RECR11.SA": {"qtd": 26,  "pm": 85.20}, 
    "VGHF11.SA": {"qtd": 340, "pm": 9.25}, 
    "VISC11.SA": {"qtd": 18,  "pm": 110.50},  
    "XPML11.SA": {"qtd": 31,  "pm": 112.40}, 
    "BTCI11.SA": {"qtd": 205, "pm": 10.05}, 
    "HGLG11.SA": {"qtd": 31,  "pm": 162.50},  
    "KNCR11.SA": {"qtd": 98,  "pm": 102.80}
}

@st.cache_data(ttl=60)
def sincronizar_b3(tickers):
    precos = {}
    for t in tickers:
        try:
            ticker_yf = yf.Ticker(t)
            precos[t] = ticker_yf.fast_info['last_price']
        except: precos[t] = 0.0
    return precos

# --- PROCESSAMENTO INTELIGENTE ---
cotacoes = sincronizar_b3(list(carteira_dados.keys()))
detalhes = []
total_investido = 0
total_atual = 0

for t, info in carteira_dados.items():
    v_investido = info['qtd'] * info['pm']
    v_atual = info['qtd'] * cotacoes[t]
    total_investido += v_investido
    total_atual += v_atual
    
    detalhes.append({
        "ATIVO": t.replace(".SA", ""),
        "QTD": info['qtd'],
        "PM": info['pm'],
        "COTAÇÃO": cotacoes[t],
        "INVESTIDO": v_investido,
        "ATUAL": v_atual,
        "PVP": v_atual / v_investido if v_investido > 0 else 0
    })

df = pd.DataFrame(detalhes)
df['PESO (%)'] = (df['ATUAL'] / total_atual) * 100

# --- LAYOUT DO TERMINAL ---
st.markdown("<h1 style='color: #C5A059;'>XP PRIVATE | INTELLIGENCE</h1>", unsafe_allow_html=True)
st.caption(f"🛰️ Conexão B3 Ativa • {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Métricas de Topo
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Investido", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("📈 Patrimônio Atual", f"R$ {total_atual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
          delta=f"{((total_atual/total_investido)-1)*100:.2f}%")
c3.metric("💸 Resultado (R$)", f"R$ {(total_atual - total_investido):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c4.metric("📊 Yield Est. (Mês)", f"R$ {total_atual*0.0096:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("📊 Alocação e Performance")
    fig = px.sunburst(df, path=['ATIVO'], values='ATUAL', color='PESO (%)', 
                     color_continuous_scale='YlOrBr')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🎯 Oportunidades do Dia")
    # Algoritmo de Rebalanceamento Simples
    # Indica compra para ativos com menor peso ou que estão abaixo do preço médio
    oportunidades = df.sort_values(by='PESO (%)').head(3)
    
    for _, row in oportunidades.iterrows():
        st.markdown(f"""
        <div class="opportunity-card">
            <small style='color: #00FF88;'>▲ OPORTUNIDADE DE APORTE</small><br>
            <strong>{row['ATIVO']}</strong> está com apenas {row['PESO (%)']:.1f}% da sua carteira.<br>
            Cotação atual: <b>R$ {row['COTAÇÃO']:.2f}</b>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 Dica: Foque em ativos com PVP abaixo de 1.00 para equilibrar seu preço médio.")

# Tabela detalhada
st.markdown("### 📋 Visão Detalhada da Custódia")
st.dataframe(df.style.format({"PM": "R$ {:.2f}", "COTAÇÃO": "R$ {:.2f}", "INVESTIDO": "R$ {:.2f}", "ATUAL": "R$ {:.2f}", "PESO (%)": "{:.1f}%"}), use_container_width=True)
