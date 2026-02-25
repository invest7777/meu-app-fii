import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão de Portfólio", layout="wide", page_icon="📊")

# --- CSS PARA CORES E LAYOUT ---
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    div[data-testid="stMetric"] {
        background-color: #E0F7FA;
        border-radius: 10px;
        padding: 10px;
        border-left: 5px solid #00BCD4;
    }
    .stTable { border: 1px solid #f0f2f6; border-radius: 10px; }
    h1, h2, h3 { color: #333333; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS DE EXEMPLO (CONFORME A TABELA DA IMAGEM) ---
data = {
    "Project": ["Community Survey", "Email Campaign", "Room Survey", "Support Mobile", "Track Upgrades"],
    "Manager": ["Elsa H.", "Elsa H.", "Elsa H.", "Elsa H.", "Elsa H."],
    "Start": ["01-Dec-23", "16-Sep-23", "20-Sep-23", "01-Oct-23", "25-Aug-23"],
    "Progress": [9%, 100%, 45%, 70%, 100%],
    "Effort/Hours": [445, 206, 1211, 450, 1005],
    "Tasks": [30, 24, 27, 10, 7]
}
df = pd.DataFrame(data)

# --- LAYOUT SUPERIOR (MÉTRICAS E GRÁFICOS) ---
st.title("📊 Painel de Desempenho do Investimento do Portfólio")

col_metrics, col_donut1, col_bar, col_donut2 = st.columns([1, 2, 3, 2])

with col_metrics:
    st.metric("Projetos", "20")
    st.metric("Tarefas", "18K")
    st.metric("Completas", "6.398")
    st.metric("Restantes", "11K")

with col_donut1:
    st.write("**Progresso do Projeto**")
    fig1 = px.pie(values=[10, 40, 50], names=["Iniciado", "Em Progresso", "Concluído"], 
                 hole=0.6, color_discrete_sequence=["#00BCD4", "#1A237E", "#E0F7FA"])
    fig1.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig1, use_container_width=True)

with col_bar:
    st.write("**Esforço por Projeto**")
    fig2 = px.bar(df, x="Project", y="Effort/Hours", color_discrete_sequence=["#00BCD4"])
    fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
    st.plotly_chart(fig2, use_container_width=True)

with col_donut2:
    st.write("**Projetos por Gestor**")
    fig3 = px.pie(df, values='Tasks', names='Project', hole=0.6, 
                 color_discrete_sequence=px.colors.sequential.GnBu_r)
    fig3.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- TABELA DETALHADA INFERIOR ---
st.subheader("📋 Detalhamento de Ativos e Tarefas")
st.table(df)

# Rodapé informativo
st.caption("⚠️ Dados simulados baseados no layout de gestão de projetos enviado.")
