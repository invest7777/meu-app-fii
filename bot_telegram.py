import telebot
import yfinance as yf
import matplotlib
matplotlib.use('Agg') # Necessário para rodar no servidor do GitHub
import matplotlib.pyplot as plt
from datetime import datetime
import io

# --- CONFIGURAÇÕES ---
TOKEN = "8714454678:AAHd_tbtINcXmG31yHF5W7AnY4fnypQLqsQ"
CHAT_ID = "5161568304"
bot = telebot.TeleBot(TOKEN)

# Sua carteira ATUALIZADA (Quantidade de cotas para totalizar R$ 29.773,26)
# IMPORTANTE: Se você comprou ou vendeu cotas, ajuste os números abaixo:
carteira_cotas = {
    "MXRF11.SA": 185, "RECR11.SA": 24, "VGHF11.SA": 315, 
    "VISC11.SA": 17,  "XPML11.SA": 28, "BTCI11.SA": 195, 
    "HGLG11.SA": 29,  "KNCR11.SA": 92
}

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def enviar_relatorio_final():
    try:
        total_atual = 0
        valores_para_grafico = {}
        corpo_msg = "🏛 *INVESTMENT BANK - CONSOLIDADO*\n"
        corpo_msg += f"📅 _{datetime.now().strftime('%d/%m/%Y %H:%M')}_\n\n"
        
        print("📊 Sincronizando preços com a B3...")
        for ticker, qtd in carteira_cotas.items():
            fii = yf.Ticker(ticker)
            preco_atual = fii.fast_info['last_price']
            subtotal = preco_atual * qtd
            total_atual += subtotal
            
            nome_limpo = ticker.replace(".SA", "")
            valores_para_grafico[nome_limpo] = subtotal
            
            # Identifica tendência do dia
            variacao = fii.info.get('regularMarketChangePercent', 0)
            emoji = "📈" if variacao >= 0 else "📉"
            
            corpo_msg += f"{emoji} *{nome_limpo}*\n"
            corpo_msg += f"   └ {formatar_br(preco_atual)} | Total: *{formatar_br(subtotal)}*\n"

        # Mensagem do patrimônio total
        corpo_msg += f"\n💰 *PATRIMÔNIO TOTAL:* \n`{formatar_br(total_atual)}`"

        # --- GERAR GRÁFICO ---
        plt.figure(figsize=(8, 7))
        plt.pie(valores_para_grafico.values(), labels=valores_para_grafico.keys(), 
                autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title(f"Alocação de Ativos - {datetime.now().strftime('%d/%m/%y')}")
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # --- ENVIAR PARA O TELEGRAM ---
        # 1. Envia o Gráfico de Pizza
        bot.send_photo(CHAT_ID, buf, caption="📊 *Divisão de Patrimônio Atual*", parse_mode="Markdown")
        
        # 2. Busca Notícias e Envia Detalhamento
        try:
            feed = yf.Ticker("^BVSP").news[:3]
            if feed:
                corpo_msg += "\n\n📰 *MERCADO AGORA:*"
                for n in feed:
                    corpo_msg += f"\n• [{n['title'][:55]}...]({n['link']})"
        except: pass

        bot.send_message(CHAT_ID, corpo_msg, parse_mode="Markdown", disable_web_page_preview=True)
        print(f"✅ Relatório enviado! Total calculado: {total_atual}")

    except Exception as e:
        print(f"❌ Erro na sincronização: {e}")

if __name__ == "__main__":
    enviar_relatorio_final()
