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
CHAT_ID = "5161568304" # IMPORTANTE: Se for grupo, deve começar com sinal de menos (-)
bot = telebot.TeleBot(TOKEN)

# Valores da sua carteira (R$ 29.773,28)
carteira_valores = {
    "MXRF11": 2001.24, "RECR11": 2090.66, "VGHF11": 3009.60,
    "VISC11": 2097.03, "XPML11": 3448.44, "BTCI11": 2008.10,
    "HGLG11": 5037.76, "KNCR11": 10080.45
}

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def enviar_diagnostico():
    try:
        print(f"🚀 Iniciando envio para o ID: {CHAT_ID}")
        
        # PASSO 1: Teste de conexão simples (Texto)
        bot.send_message(CHAT_ID, "🔌 *Conexão Online:* O seu App de Banco está tentando enviar o relatório agora...")
        
        total = sum(carteira_valores.values())
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # PASSO 2: Gerar Gráfico
        plt.style.use('dark_background')
        plt.figure(figsize=(8, 6))
        plt.pie(carteira_valores.values(), labels=carteira_valores.keys(), autopct='%1.1f%%', colors=plt.cm.Paired.colors)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        # PASSO 3: Enviar Foto
        caption = f"🏛 *RELATÓRIO ATUALIZADO*\n💰 Patrimônio: `{formatar_br(total)}`"
        bot.send_photo(CHAT_ID, buf, caption=caption, parse_mode="Markdown")
        
        print("✅ Tudo enviado com sucesso!")

    except Exception as e:
        print(f"❌ ERRO NO ENVIO: {e}")
        # Se falhar aqui, o GitHub Actions ficará VERMELHO e mostrará o motivo exato
        sys.exit(1) 

if __name__ == "__main__":
    enviar_diagnostico()
