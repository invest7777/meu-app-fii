import os
import telebot
import yfinance as yf

# Busca as chaves que você salvou no GitHub Secrets
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def enviar_cotacao():
    try:
        # Busca cotação do Dólar (USDBRL=X)
        data = yf.Ticker("USDBRL=X")
        preco = data.history(period="1d")['Close'].iloc[-1]
        
        mensagem = f"🤖 *Relatório Diário*\n\n💵 Cotação do Dólar: R$ {preco:.2f}"
        
        bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
        print("Mensagem enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")

if __name__ == "__main__":
    enviar_cotacao()
