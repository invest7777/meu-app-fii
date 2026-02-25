import telebot
import yfinance as yf
import time

# --- CONFIGURAÇÕES ---
TOKEN = "8714454678:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "5161568304"
bot = telebot.TeleBot(TOKEN)

# Valores exatos do seu print "Minha Carteira de FIIs"
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

def enviar_resumo():
    total_patrimonio = sum(carteira.values())
    
    mensagem = "🏦 *RELATÓRIO REAL - CARTEIRA FII*\n"
    mensagem += "------------------------------------\n\n"
    
    for ticker, valor in carteira.items():
        mensagem += f"🔹 *{ticker.replace('.SA', '')}*: R$ {valor:,.2f}\n"
    
    mensagem += "\n------------------------------------\n"
    mensagem += f"💰 *Total na Carteira:* R$ {total_patrimonio:,.2f}\n"
    
    try:
        bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
        print("Relatório enviado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    enviar_resumo()
