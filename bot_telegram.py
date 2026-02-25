import telebot
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import io

# --- CONFIGURAÇÕES ---
TOKEN = "8714454678:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "5161568304"
bot = telebot.TeleBot(TOKEN)

# Sua carteira (Quantidade de cotas)
carteira_cotas = {
    "MXRF11.SA": 204, "RECR11.SA": 26, "VGHF11.SA": 340, 
    "VISC11.SA": 18,  "XPML11.SA": 31, "BTCI11.SA": 205, 
    "HGLG11.SA": 31,  "KNCR11.SA": 98
}

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_grafico(dados_carteira):
    df = pd.DataFrame(list(dados_carteira.items()), columns=['FII', 'Valor'])
    df['FII'] = df['FII'].str.replace('.SA', '')
    
    plt.figure(figsize=(8, 6))
    plt.pie(df['Valor'], labels=df['FII'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title(f"Distribuição da Carteira - {datetime.now().strftime('%d/%m/%y')}")
    
    # Salva o gráfico na memória para enviar ao Telegram
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

def enviar_relatorio_premium():
    try:
        total_atual = 0
        valores_para_grafico = {}
        corpo_msg = "🏛 *INVESTMENT BANK - CONSOLIDADO*\n"
        corpo_msg += f"📅 _{datetime.now().strftime('%d/%m/%Y %H:%M')}_\n\n"
        
        print("📊 Buscando preços na B3...")
        for ticker, qtd in carteira_cotas.items():
            fii = yf.Ticker(ticker)
            preco_atual = fii.fast_info['last_price']
            subtotal = preco_atual * qtd
            total_atual += subtotal
            valores_para_grafico[ticker] = subtotal
            
            variacao = fii.info.get('regularMarketChangePercent', 0)
            emoji = "📈" if variacao >= 0 else "📉"
            corpo_msg += f"{emoji} *{ticker.replace('.SA', '')}*\n   └ {formatar_br(preco_atual)} | Total: *{formatar_br(subtotal)}*\n"

        corpo_msg += f"\n💰 *PATRIMÔNIO TOTAL:* \n`{formatar_br(total_atual)}`"
        
        # 1. Enviar o Gráfico
        grafico = gerar_grafico(valores_para_grafico)
        bot.send_photo(CHAT_ID, grafico, caption="📊 *Sua Alocação Atual*", parse_mode="Markdown")
        
        # 2. Enviar o Relatório e Notícias
        try:
            feed = yf.Ticker("^BVSP").news[:3]
            if feed:
                corpo_msg += "\n\n📰 *NOTÍCIAS DO MERCADO:*"
                for n in feed:
                    corpo_msg += f"\n• [{n['title'][:55]}...]({n['link']})"
        except: pass

        bot.send_message(CHAT_ID, corpo_msg, parse_mode="Markdown", disable_web_page_preview=True)
        print("✅ Relatório e Gráfico enviados!")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    enviar_relatorio_premium()
