import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Minha Carteira FII", layout="wide")

# Seus dados reais conforme o último patrimônio de R$ 31.773,28
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

resumo_data = []
total_patrimonio = 0
total_dividendos_estimados = 0

# Barra de progresso para você saber que o app está trabalhando
progresso = st.progress(0)
status_texto = st.empty()

for i, (ticker, valor_investido) in enumerate(carteira_atual.items()):
    status_texto.text(f"Consultando {ticker}...")
    fundo = yf.Ticker(ticker)
    
    # Pausa estratégica para evitar o erro de bloqueio (Rate Limit)
    time.sleep(1)
    
    try:
        info = fundo.info
        preco = info.get('currentPrice', 1)
        vp = info.get('bookValue', 1)
        div = info.get('lastDividendValue', 0)
    except:
        preco, vp, div = 1, 1, 0
    
    qtd_cotas = valor_investido / preco
    renda_fundo = qtd_cotas * div
    p_vp = preco / vp
    
    total_patrimonio += valor_investido
    total_dividendos_estimados += renda_fundo
    
    resumo_data.append({
        "Fundo": ticker.replace(".SA", ""),
        "Investido": valor_investido,
        "Renda Est.": renda_fundo,
        "P/VP": round(p_vp, 2)
    })
    progresso.progress((i + 1) / len(carteira_atual))

status_texto.empty()
progresso.empty()

# Painel Principal
col1, col2, col3 = st.columns(3)
col1.metric("Patrimônio Total", f"R$ {total_patrimonio:,.2f}")
col2.metric("Renda Mensal Est.", f"R$ {total_dividendos_estimados:,.2f}")
col3.metric("Yield Médio", f"{(total_dividendos_estimados/total_patrimonio)*100:.2f}%")

st.divider()

# Tabela formatada
df = pd.DataFrame(resumo_data)
st.subheader("Detalhamento da Carteira")
st.dataframe(df.style.format({
    "Investido": "R$ {:.2f}",
    "Renda Est.": "R$ {:.2f}"
}), use_container_width=True)

# Gráfico de Barras estável
st.subheader("Peso de cada Fundo no Patrimônio")
st.bar_chart(df.set_index("Fundo")["Investido"])
