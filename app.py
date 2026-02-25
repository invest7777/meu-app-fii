import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Portfólio", layout="wide", page_icon="📊")

# --- CSS PARA CORES E LAYOUT ---
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        border-left: 5px solid #00BCD4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 { color: #333333; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS CORRIGIDOS (SEM SÍMBOLO DE %) ---
data = {
    "Project": ["Community Survey", "Email Campaign", "Room Survey", "Support Mobile", "Track Upgrades"],
    "Manager": ["Elsa H.", "Elsa H.", "Elsa H.", "Elsa H.", "Elsa H."],
    "Start": ["01-Dec-23", "16-Sep-23", "20-Sep-23", "01-Oct-23", "25-Aug-23"],
    "Progress (%)": [9, 100, 45, 70, 100],  # Corrigido aqui (apenas números)
    "Effort (h)": [450, 120, 310, 200, 80],
    "Tasks": [12, 5, 8, 15, 3]
}
df = pd.DataFrame(data)

# --- LAYOUT SUPERIOR ---
st.title("📊 Painel de Desempenho do Portfólio")

col_metrics, col_donut1, col_bar, col_donut2 = st.columns([1, 1.5, 2, 1.5])

with col_metrics:
    st.metric("Projetos", "20")
    st.metric("Tarefas", "18K")
    st.metric("Completas", "6.398")
    st.metric("Restantes", "11K")

with col_donut1:
    st.write("**Progresso Médio**")
    fig1 = px.pie(values=[45, 55], names=["Concluído", "Pendente"], hole=0.7, 
                 color_discrete_sequence=["#00BCD4", "#E0F7FA"])
    fig1.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig1, use_container_width=True)

with col_bar:
    st.write("**Esforço por Projeto (Horas)**")
    fig2 = px.bar(df, x="Project", y="Effort (h)", color="Project", 
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=250)
    st.plotly_chart(fig2, use_container_width=True)

with col_donut2:
    st.write("**Tarefas por Projeto**")
    fig3 = px.pie(df, values='Tasks', names='Project', hole=0.7, 
                 color_discrete_sequence=px.colors.sequential.GnBu_r)
    fig3.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- TABELA DETALHADA ---
st.subheader("📋 Detalhamento de Ativos e Metas")
# Formata a coluna de progresso para exibir o % de novo, mas apenas visualmente
st.dataframe(df.style.format({"Progress (%)": "{}%"}), use_container_width=True)
