import telebot
from telebot import types
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import io

# --- CONFIGURAÇÕES ---
TOKEN = "8714454678:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "5161568304"
bot = telebot.TeleBot(TOKEN)

# Sua carteira real no banco (Total: R$ 29.773,26)
carteira_valores = {
    "MXRF11": 1850.50, "RECR11": 2040.66, "VGHF11": 2809.60, 
    "VISC11": 1997.03, "XPML11": 3248.44, "BTCI11": 1808.10, 
    "HGLG11": 4837.76, "KNCR11": 11181.17
}

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def criar_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_carteira = types.InlineKeyboardButton("💰 Minha Carteira", callback_data="ver_carteira")
    btn_grafico = types.InlineKeyboardButton("📊 Gráfico de Alocação", callback_data="ver_grafico")
    btn_noticias = types.InlineKeyboardButton("📰 Notícias do Mundo", callback_data="ver_noticias")
    markup.add(btn_carteira, btn_grafico, btn_noticias)
    return markup

def buscar_noticias_mundo():
    try:
        # Busca notícias globais via Yahoo Finance
        feed = yf.Ticker("^BVSP").news[:5] # Pega as 5 principais notícias
        txt = "🌍 *NOTÍCIAS EM TEMPO REAL*\n\n"
        for n in feed:
            txt += f"• [{n['title'][:60]}...]({n['link']})\n\n"
        return txt
    except:
        return "⚠️ Não foi possível carregar as notícias agora."

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "ver_carteira":
        total = sum(carteira_valores.values())
        msg = "🏛 *INVESTMENT BANK - PATRIMÔNIO*\n\n"
        for ticker, valor in carteira_valores.items():
            msg += f"🔹 *{ticker}*: {formatar_br(valor)}\n"
        msg += f"\n💰 *TOTAL ATUAL: {formatar_br(total)}*"
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown", reply_markup=criar_menu())
    
    elif call.data == "ver_grafico":
        plt.figure(figsize=(8, 7))
        plt.pie(carteira_valores.values(), labels=carteira_valores.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title(f"Distribuição Bancária - {datetime.now().strftime('%d/%m/%y')}")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        bot.send_photo(CHAT_ID, buf, caption="📊 *Sua Divisão de Ativos*", reply_markup=criar_menu())

    elif call.data == "ver_noticias":
        noticias = buscar_noticias_mundo()
        bot.send_message(CHAT_ID, noticias, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=criar_menu())

def iniciar_app():
    # Mensagem de boas-vindas estilo banco
    msg_inicial = "👋 *Bem-vindo ao seu Private Bank!*\n\nO que deseja consultar hoje?"
    bot.send_message(CHAT_ID, msg_inicial, parse_mode="Markdown", reply_markup=criar_menu())

if __name__ == "__main__":
    iniciar_app()
