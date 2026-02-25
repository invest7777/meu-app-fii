import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Minha Carteira FII", layout="wide")

# Dados do seu patrimônio atual (conforme seu print)
carteira_atual = {
    "MXRF11.SA": 2001.24,
    "RECR11.SA": 2090.66,
    "VGHF11.SA": 3009.60,
    "VISC11.SA": 2097.03,
    "XPML11.SA": 3448.44,
    "BTCI11.SA": 2008.10,
    "HGLG11.SA": 5037.76,
    "KNCR11.SA": 10080.45
}

st.title("📱 Meu App de Investimentos")

# Buscando dados em tempo real
resumo_data = []
total_patrimonio = 0
total_dividendos_estimados = 0

for ticker, valor_investido in carteira_atual.items():
    fundo = yf.Ticker(ticker)
    preco = fundo.info.get('currentPrice', 1)
    div = fundo.info.get('lastDividendValue', 0)
    qtd_cotas = valor_investido / preco
    renda_fundo = qtd_cotas * div
    
    total_patrimonio += valor_investido
    total_dividendos_estimados += renda_fundo
    
    resumo_data.append({
        "Fundo": ticker.replace(".SA", ""),
        "Investido": f"R$ {valor_investido:,.2f}",
        "Renda Est.": f"R$ {renda_fundo:,.2f}",
        "P/VP": round(preco / fundo.info.get('bookValue', 1), 2)
    })

# Cabeçalho com métricas
col1, col2, col3 = st.columns(3)
col1.metric("Patrimônio Total", f"R$ {total_patrimonio:,.2f}")
col2.metric("Renda Mensal Est.", f"R$ {total_dividendos_estimados:,.2f}")
col3.metric("Yield Médio", f"{(total_dividendos_estimados/total_patrimonio)*100:.2f}%")

st.divider()

# Tabela e Gráfico
df = pd.DataFrame(resumo_data)
st.subheader("Detalhamento da Carteira")
st.dataframe(df, use_container_width=True)

st.subheader("Peso de cada Fundo no Patrimônio")
st.pie_chart(data=pd.DataFrame({"Valor": carteira_atual.values()}, index=carteira_atual.keys()), values="Valor")
