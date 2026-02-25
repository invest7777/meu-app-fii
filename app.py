import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Gestor Pro FII", layout="wide", initial_sidebar_state="expanded")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DA CARTEIRA ---
carteira_atual = {
    "MXRF11.SA": 2001.24, "RECR11.SA": 2090.66, "VGHF11.SA": 3009.60, 
    "VISC11.SA": 2097.03, "XPML11.SA": 3448.44, "BTCI11.SA": 2008.10, 
    "HGLG11.SA": 5037.76, "KNCR11.SA": 10080.45
}

st.title("📊 Gestor de Inteligência Financeira")

# --- SIDEBAR: APORTE INTELIGENTE ---
st.sidebar.header("🎯 Novo Investimento")
valor_aporte = st.sidebar.number_input("Quanto deseja investir hoje? (R$)", min_value=0.0, value=0.0)

# --- PROCESSAMENTO ---
resumo_data = []
total_patrimonio = 0
total_div = 0

with st.spinner('Atualizando dados do mercado...'):
    for ticker, investido in carteira_atual.items():
        fundo = yf.Ticker(ticker)
        time.sleep(0.5) # Pausa menor para ser mais rápido
        try:
            info = fundo.info
            p = info.get('currentPrice', 1)
            vp = info.get('bookValue', 1)
            d = info.get('lastDividendValue', 0)
        except:
            p, vp, d = 1, 1, 0
        
        pvp = p / vp
        renda = (investido / p) * d
        total_patrimonio += investido
        total_div += renda
        
        # Lógica do Semáforo
        status = "🟢 COMPRAR" if pvp < 1.0 else "🟡 NEUTRO" if pvp < 1.05 else "🔴 CARO"
        
        resumo_data.append({
            "Fundo": ticker.replace(".SA", ""),
            "Preço Atual": p,
            "P/VP": round(pvp, 2),
            "Renda Mensal": renda,
            "Sugestão": status
        })

# --- DASHBOARD DE MÉTRICAS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Patrimônio total", f"R$ {total_patrimonio:,.2f}")
c2.metric("Renda Mensal", f"R$ {total_div:,.2f}")
c3.metric("Renda Diária (Média)", f"R$ {total_div/30:,.2f}")
c4.metric("Yield da Carteira", f"{(total_div/total_patrimonio)*100:.2f}%")

st.divider()

# --- TABELA INTERATIVA ---
df = pd.DataFrame(resumo_data)
st.subheader("📋 Análise Estratégica da Carteira")
st.dataframe(df.style.applymap(lambda x: 'color: green' if x == '🟢 COMPRAR' else ('color: red' if x == '🔴 CARO' else 'color: orange'), subset=['Sugestão']), use_container_width=True)

# --- RECOMENDAÇÃO DE APORTE ---
if valor_aporte > 0:
    st.success(f"### 💡 Onde alocar seus R$ {valor_aporte:,.2f}:")
    melhor_fundo = df.sort_values(by="P/VP").iloc[0]
    st.write(f"Com base no P/VP, o fundo mais barato hoje é o **{melhor_fundo['Fundo']}**. Você poderia comprar aproximadamente **{int(valor_aporte // melhor_fundo['Preço Atual'])} cotas** para fortalecer sua renda.")

st.subheader("📈 Concentração de Patrimônio")
st.bar_chart(df.set_index("Fundo")["Renda Mensal"])
