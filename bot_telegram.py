import telebot
import yfinance as yf
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from datetime import datetime
import io
import sys

# --- CONFIGURAÇÕES ---
TOKEN = "8714454678:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "5161568304"
bot = telebot.TeleBot(TOKEN)

carteira_valores = {
    "MXRF11": 1850.50, "RECR11": 2040.66, "VGHF11": 2809.60, 
    "VISC11": 1997.03, "XPML11": 3248.44, "BTCI11": 1808.10, 
    "HGLG11": 4837.76, "KNCR11": 11181.17
}

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def enviar_relatorio_emergencia():
    try:
        total = sum(carteira_valores.values())
        divs = total * 0.0095
        
        # Gerar Gráfico
        plt.style.use('dark_background')
        plt.figure(figsize=(8, 6))
        plt.pie(carteira_valores.values(), labels=carteira_valores.keys(), autopct='%1.1f%%')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Montar texto
        msg = f"🏛 *RELATÓRIO DE TESTE*\nTotal: {formatar_br(total)}\nDivs: {formatar_br(divs)}"

        print(f"🚀 Tentando enviar para o ID: {CHAT_ID}...")
        
        # TESTE: Envia primeiro apenas um texto simples para ver se o ID está certo
        bot.send_message(CHAT_ID, "🔌 Teste de Conexão: O robô está online!")
        
        # Envia a foto
        bot.send_photo(CHAT_ID, buf, caption=msg, parse_mode="Markdown")
        
        print("✅ Comandos de envio finalizados sem erros no Python.")

    except Exception as e:
        print(f"❌ ERRO IDENTIFICADO: {e}")
        sys.exit(1) # Força o GitHub a ficar VERMELHO se falhar

if __name__ == "__main__":
    enviar_relatorio_emergencia()
