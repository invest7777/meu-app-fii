     import telebot
import yfinance as yf
import time

# --- CONFIGURAÇÕES ---
TOKEN = "7953321564:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "1430932470"
bot = telebot.TeleBot(TOKEN)

# Sua carteira real
carteira = {
    "MXRF11.SA": 2001.24, "RECR11.SA": 2090.66, "VGHF11.SA": 3009.60, 
    "VISC11.SA": 2097.03, "XPML11.SA": 3448.44, "BTCI11.SA": 2008.10, 
    "HGLG11.SA": 5037.76, "KNCR11.SA": 10080.45
}

def enviar_resumo():
    total_patrimonio = 0
    total_renda = 0
    mensagem = "🏦 *RELATÓRIO DIÁRIO - CARTEIRA FII*\n"
    mensagem += "------------------------------------\n\n"
    
    for ticker, valor_investido in carteira.items():
        try:
            fundo = yf.Ticker(ticker)
            time.sleep(1) 
            preco = fundo.info.get('currentPrice', 1)
            dividendo = fundo.info.get('lastDividendValue', 0)
            
            renda_fundo = (valor_investido / preco) * dividendo
            total_patrimonio += valor_investido
            total_renda += renda_fundo
            
            mensagem += f"🔹 *{ticker.replace('.SA', '')}*: R$ {valor_investido:,.2f}\n"
        except:
            continue
    
    mensagem += "\n------------------------------------\n"
    mensagem += f"💰 *Total Investido:* R$ {total_patrimonio:,.2f}\n"
    mensagem += f"💸 *Renda Mensal Est.:* R$ {total_renda:,.2f}\n"
    
    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")

if __name__ == "__main__":
    enviar_resumo()
