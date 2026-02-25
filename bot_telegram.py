import telebot
import yfinance as yf
import time

# --- CONFIGURAÇÕES ATUALIZADAS ---
TOKEN = "8714454678:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "5161568304"
bot = telebot.TeleBot(TOKEN)

# Sua carteira com os valores de ~29 mil
carteira = {
    "MXRF11.SA": 1880.50, "RECR11.SA": 1965.20, "VGHF11.SA": 2829.10, 
    "VISC11.SA": 1971.20, "XPML11.SA": 3241.55, "BTCI11.SA": 1887.60, 
    "HGLG11.SA": 4735.40, "KNCR11.SA": 9475.00
}

def enviar_resumo():
    total_patrimonio = 0
    mensagem = "🏦 *RELATÓRIO DIÁRIO - CARTEIRA FII*\n\n"
    
    for ticker, valor in carteira.items():
        total_patrimonio += valor
        mensagem += f"🔹 *{ticker.replace('.SA', '')}*: R$ {valor:,.2f}\n"
    
    mensagem += f"\n💰 *Total na Carteira: R$ {total_patrimonio:,.2f}*"
    
    try:
        bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
        print("Mensagem enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar: {e}")

if __name__ == "__main__":
    enviar_resumo()
