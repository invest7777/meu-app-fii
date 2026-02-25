import time # Adicione isso no topo do arquivo com os outros imports

# ... dentro do seu loop for ...
for ticker, valor_investido in carteira_atual.items():
    fundo = yf.Ticker(ticker)
    
    # Adicionando uma pequena pausa de 1 segundo para não ser bloqueado
    time.sleep(1) 
    
    # Tenta pegar o preço, se falhar usa o valor 1 para não travar o app
    try:
        info = fundo.info
        preco = info.get('currentPrice', 1)
        vp = info.get('bookValue', 1)
        div = info.get('lastDividendValue', 0)
    except:
        preco, vp, div = 1, 1, 0
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
st.subheader("Peso de cada Fundo no Patrimônio")
# Criando os dados do gráfico de forma simplificada
df_grafico = pd.DataFrame({
    'Fundo': list(carteira_atual.keys()),
    'Valor': list(carteira_atual.values())
})
st.bar_chart(df_grafico.set_index('Fundo'))
