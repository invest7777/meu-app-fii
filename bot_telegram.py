import telebot
import yfinance as yf
import time

# --- CONFIGURAÇÕES ---
TOKEN = "7953321564:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "1430932470"
bot = telebot.TeleBot(TOKEN)

# Sua carteira de R$ 31.773,28
carteira = {
    "MXRF11.SA": 2001.24, "RECR11.SA": 2090.66, "VGHF11.SA": 3009.60, 
    "VISC11.SA": 2097.03, "XPML11.SA": 3448.44, "BTCI11.SA": 2008.10, 
    "HGLG11.SA": 5037.76, "KNCR11.SA": 10080.45
}

def enviar_resumo():
    total_patrimonio = 0
    mensagem = "🏦 *RELATÓRIO DIÁRIO - CARTEIRA FII*\n\n"
    
    for ticker, valor in carteira.items():
        try:
            fundo = yf.Ticker(ticker)
            time.sleep(1) 
            total_patrimonio += valor
            mensagem += f"🔹 *{ticker.replace('.SA', '')}*: R$ {valor:,.2f}\n"
        except:
            continue
    
    mensagem += f"\n💰 *Total Investido: R$ {total_patrimonio:,.2f}*"
    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")

if __name__ == "__main__":
    enviar_resumo()

