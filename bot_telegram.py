import telebot

# --- CONFIGURAÇÕES ---
TOKEN = "7953321564:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "1430932470"
bot = telebot.TeleBot(TOKEN)

# Sua carteira real
carteira = {
    "MXRF11.SA": 2001.24, 
    "RECR11.SA": 2090.66, 
    "VGHF11.SA": 3009.60, 
    "VISC11.SA": 2097.03, 
    "XPML11.SA": 3448.44, 
    "BTCI11.SA": 2008.10, 
    "HGLG11.SA": 5037.76, 
    "KNCR11.SA": 10080.45
}

def formatar_moeda(valor):
    # Formata para padrão brasileiro: 1.234,56
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def enviar_resumo():
    total_patrimonio = 0
    mensagem = "🏦 *RELATÓRIO DIÁRIO - CARTEIRA FII*\n\n"
    
    for ticker, valor in carteira.items():
        total_patrimonio += valor
        ticker_nome = ticker.replace(".SA", "")
        mensagem += f"🔹 *{ticker_nome}*: R$ {formatar_moeda(valor)}\n"
    
    total_texto = formatar_moeda(total_patrimonio)
    mensagem += f"\n💰 *Total Investido: R$ {total_texto}*"
    
    try:
        bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
        print("✅ Relatório enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")

if __name__ == "__main__":
    enviar_resumo()
