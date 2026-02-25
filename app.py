import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuração de estilo "Premium"
st.set_page_config(page_title="Investidor Pro", layout="wide")

# CSS para fontes e cores de App de Investimento
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    .metric-card { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# Dados exatos da sua carteira
carteira = {
    "MXRF11.SA": 2001.24, "RECR11.SA": 2090.66, "VGHF11.SA": 3009.60, 
    "VISC11.SA": 2097.03, "XPML11.SA": 3448.44, "BTCI11.SA": 2008.10, 
    "HGLG11.SA": 5037.76, "KNCR11.SA": 10080.45
}

# Função para formatar moeda no padrão BR (1.234,56)
def formata_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

st.title("🏦 Minha Carteira Profissional")

resumo = []
total_investido = 0
total_mensal = 0

# Processamento
with st.spinner('Sincronizando com a B3...'):
    for ticker, valor in carteira.items():
        fundo = yf.Ticker(ticker)
        time.sleep(0.6)
        try:
            p = fundo.info.get('currentPrice', 1)
            d = fundo.info.get('lastDividendValue', 0)
            total_investido += valor
            renda_estimada = (valor / p) * d
            total_mensal += renda_estimada
            resumo.append({
                "Ativo": ticker.replace(".SA", ""), 
                "Patrimônio": valor, 
                "Renda Mensal": renda_estimada
            })
        except:
            continue

df = pd.DataFrame(resumo)

# --- DASHBOARD DE MÉTRICAS (CARTÕES) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Patrimônio Total", formata_br(total_investido))
with col2:
    st.metric("Dividendos Estimados", formata_br(total_mensal))
with col3:
    yield_medio = (total_mensal / total_investido) * 100
    st.metric("Yield Médio", f"{yield_medio:.2f}%")

st.markdown("---")

# --- GRÁFICOS LADO A LADO ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Distribuição de Patrimônio")
    st.bar_chart(df.set_index("Ativo")["Patrimônio"], color="#1f77b4")

with col_right:
    st.subheader("💸 Geração de Renda por Fundo")
    st.bar_chart(df.set_index("Ativo")["Renda Mensal"], color="#2ca02c")

st.markdown("---")

# --- TABELA PROFISSIONAL ---
st.subheader("📝 Extrato Detalhado")
df_formatado = df.copy()
df_formatado["Patrimônio"] = df_formatado["Patrimônio"].apply(formata_br)
df_formatado["Renda Mensal"] = df_formatado["Renda Mensal"].apply(formata_br)
st.dataframe(df_formatado, use_container_width=True, hide_index=True)
