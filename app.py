import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Felicidade 2021", layout="wide")

# Estilização personalizada para fundo escuro
st.markdown("""
    <style>
        .main {
            background-color: #111111;
            color: #FFFFFF;
        }
        div[data-testid="metric-container"] {
            background-color: #222222;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
        }
        h1, h2, h3, h4 {
            color: #f7931e;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard de Felicidade Mundial (2021)")

# Carregamento de dados
df = pd.read_csv("world-happiness-report-2021.csv")

# Filtro
regioes = df['Regional indicator'].unique()
regiao_selecionada = st.selectbox("🌍 Selecione uma região:", regioes)
df_filtrado = df[df['Regional indicator'] == regiao_selecionada]

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📌 Média de Felicidade", f"{df_filtrado['Ladder score'].mean():.2f}")
with col2:
    st.metric("💰 PIB Médio (log)", f"{df_filtrado['Logged GDP per capita'].mean():.2f}")
with col3:
    st.metric("🌎 Total de Países", len(df_filtrado))

st.markdown("---")

# Gráficos organizados em 3 colunas
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("📈 Felicidade por País")
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.plot(df_filtrado['Country name'], df_filtrado['Ladder score'], color="#f7931e", marker='o', linewidth=1)
    ax1.tick_params(axis='x', labelrotation=90, labelsize=7)
    fig1.patch.set_facecolor('#222222')
    st.pyplot(fig1)

with col5:
    st.subheader("📊 PIB per Capita")
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    ax2.bar(df_filtrado['Country name'], df_filtrado['Logged GDP per capita'], color="#f7931e")
    ax2.tick_params(axis='x', labelrotation=90, labelsize=7)
    fig2.patch.set_facecolor('#222222')
    st.pyplot(fig2)

with col6:
    st.subheader("🥧 Distribuição por Região")
    regiao_count = df['Regional indicator'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    ax3.pie(regiao_count, labels=regiao_count.index, autopct='%1.1f%%',
            colors=["#f7931e", "#444444", "#888888", "#CCCCCC"])
    fig3.patch.set_facecolor('#222222')
    st.pyplot(fig3)

st.markdown("---")

# Gráfico de dispersão interativo
st.subheader("🔵 Dispersão Interativa - Felicidade x PIB")
fig4 = px.scatter(
    df_filtrado,
    x="Logged GDP per capita",
    y="Ladder score",
    color="Country name",
    hover_name="Country name",
    title="Felicidade x PIB per capita",
    labels={
        "Logged GDP per capita": "PIB per capita (log)",
        "Ladder score": "Índice de Felicidade"
    },
    height=400,
    color_discrete_sequence=px.colors.sequential.Oranges
)
st.plotly_chart(fig4, use_container_width=True)

# Tabela final
st.subheader("📋 Tabela de Dados da Região Selecionada")
st.dataframe(df_filtrado.style.background_gradient(cmap='Oranges'))
