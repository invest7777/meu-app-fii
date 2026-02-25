import telebot
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

def enviar_relatorio_vip():
    try:
        total = sum(carteira_valores.values())
        # Estimativa de dividendos (Média de 0,95% ao mês para FIIs de tijolo/papel)
        dividendos_estimados = total * 0.0095 
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # 1. GERAR GRÁFICO PREMIUM (Com fundo escuro e cores elegantes)
        plt.style.use('dark_background')
        plt.figure(figsize=(10, 8))
        cores = ['#2ecc71', '#3498db', '#9b59b6', '#f1c40f', '#e67e22', '#e74c3c', '#1abc9c', '#34495e']
        
        plt.pie(carteira_valores.values(), labels=carteira_valores.keys(), 
                autopct='%1.1f%%', startangle=140, colors=cores, 
                wedgeprops={'edgecolor': '#000000', 'linewidth': 2})
        
        plt.title(f"📊 ALOCAÇÃO DE ATIVOS\nBanco de Investimentos", color='white', fontsize=16, pad=20)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=False, facecolor='#121212')
        buf.seek(0)
        plt.close()
        
        # 2. MONTAR TEXTO DO APP
        msg = f"🏛 *PRIVATE BANKING - CONSOLIDADO*\n"
        msg += f"📅 _{data_hora}_\n\n"
        
        for ticker, valor in carteira_valores.items():
            msg += f"🔹 *{ticker}*: {formatar_br(valor)}\n"
            
        msg += f"\n💰 *PATRIMÔNIO TOTAL:* \n`{formatar_br(total)}`"
        
        # Seção de Proventos
        msg += f"\n\n💸 *ESTIMATIVA DE DIVIDENDOS (MÊS):*\n`{formatar_br(dividendos_estimados)}`"
        msg += f"\n_Rendimento médio est. em 0,95% a.m._"

        # 3. BUSCAR NOTÍCIAS GLOBAIS
        try:
            feed = yf.Ticker("^BVSP").news[:4]
            if feed:
                msg += "\n\n📰 *NOTÍCIAS DO MUNDO (AGORA):*"
                for n in feed:
                    msg += f"\n• [{n['title'][:55]}...]({n['link']})"
        except: pass

        # 4. ENVIAR TUDO
        bot.send_photo(CHAT_ID, buf, caption=msg, parse_mode="Markdown", disable_web_page_preview=True)
        print(f"✅ Relatório VIP enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    enviar_relatorio_vip()
