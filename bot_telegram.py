import telebot
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÕES ---
TOKEN = "8714454678:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "5161568304"
bot = telebot.TeleBot(TOKEN)

# Sua carteira ajustada para o patrimônio de R$ 31.773,28
# O robô busca o preço real na B3 e multiplica pelas cotas abaixo:
carteira_cotas = {
    "MXRF11.SA": 204, "RECR11.SA": 26, "VGHF11.SA": 340, 
    "VISC11.SA": 18,  "XPML11.SA": 31, "BTCI11.SA": 205, 
    "HGLG11.SA": 31,  "KNCR11.SA": 98
}

def formatar_br(valor):
    # Formata para padrão brasileiro: R$ 1.234,56
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def enviar_resumo():
    try:
        total_atual = 0
        corpo_msg = "🏛 *INVESTMENT BANK - CONSOLIDADO*\n"
        corpo_msg += f"📅 _{datetime.now().strftime('%d/%m/%Y %H:%M')}_\n\n"
        
        for ticker, qtd in carteira_cotas.items():
            # Busca o preço real na B3 via yfinance
            fii = yf.Ticker(ticker)
            preco_atual = fii.fast_info['last_price']
            subtotal = preco_atual * qtd
            total_atual += subtotal
            
            # Pega variação do dia para o emoji (📈 ou 📉)
            variacao = fii.info.get('regularMarketChangePercent', 0)
            emoji = "📈" if variacao >= 0 else "📉"
            
            nome = ticker.replace(".SA", "")
            corpo_msg += f"{emoji} *{nome}*\n"
            corpo_msg += f"   └ {formatar_br(preco_atual)} | Total: *{formatar_br(subtotal)}*\n"

        corpo_msg += f"\n💰 *PATRIMÔNIO TOTAL ATUALIZADO:* \n`{formatar_br(total_atual)}`"
        
        # BUSCA NOTÍCIAS REAIS DO MERCADO
        try:
            feed = yf.Ticker("^BVSP").news[:3]
            if feed:
                corpo_msg += "\n\n📰 *NOTÍCIAS DO MERCADO:*"
                for n in feed:
                    corpo_msg += f"\n• [{n['title'][:55]}...]({n['link']})"
        except:
            pass

        bot.send_message(CHAT_ID, corpo_msg, parse_mode="Markdown", disable_web_page_preview=True)
        print("✅ Relatório enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro na execução: {e}")

if __name__ == "__main__":
    enviar_resumo()
