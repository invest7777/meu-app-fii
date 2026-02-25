import yfinance as yf
import telebot
import time

# --- CONFIGURAÇÕES ---
TOKEN = "SEU_TOKEN_AQUI"
CHAT_ID = "SEU_CHAT_ID_AQUI"
bot = telebot.TeleBot(TOKEN)

carteira = {
    "MXRF11.SA": 2001.24, "RECR11.SA": 2090.66, "VGHF11.SA": 3009.60, 
    "VISC11.SA": 2097.03, "XPML11.SA": 3448.44, "BTCI11.SA": 2008.10, 
    "HGLG11.SA": 5037.76, "KNCR11.SA": 10080.45
}

def enviar_resumo():
    total_patrimonio = 0
    mensagem = "📊 *Relatório Diário de Investimentos*\n\n"
    
    for ticker, valor in carteira.items():
        fundo = yf.Ticker(ticker)
        time.sleep(1) # Evita bloqueios
        preco = fundo.info.get('currentPrice', 1)
        total_patrimonio += valor
        mensagem += f"🔹 *{ticker.replace('.SA', '')}*: R$ {valor:,.2f}\n"
    
    mensagem += f"\n💰 *Patrimônio Total: R$ {total_patrimonio:,.2f}*"
    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")

if __name__ == "__main__":
    enviar_resumo()
