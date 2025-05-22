
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Dashboard Felicidade 2021", layout="wide")
st.title("🌍 Dashboard - Relatório Mundial da Felicidade (2021)")

df = pd.read_csv("world-happiness-report-2021.csv")

# Filtro por região
regioes = df['Regional indicator'].unique()
regiao_selecionada = st.selectbox("Selecione uma região:", regioes)
df_filtrado = df[df['Regional indicator'] == regiao_selecionada]

# KPIs no topo
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.metric("Média de Felicidade", f"{df_filtrado['Ladder score'].mean():.2f}")
with col_kpi2:
    st.metric("PIB Médio (log)", f"{df_filtrado['Logged GDP per capita'].mean():.2f}")
with col_kpi3:
    st.metric("Total de Países", len(df_filtrado))

st.markdown("---")

# Gráficos de linha e barra lado a lado
col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 Score da Felicidade por País")
    fig1, ax1 = plt.subplots()
    ax1.plot(df_filtrado['Country name'], df_filtrado['Ladder score'], marker='o')
    plt.xticks(rotation=90)
    plt.ylabel('Ladder Score')
    st.pyplot(fig1)
with col2:
    st.subheader("📊 PIB per Capita por País")
    fig2, ax2 = plt.subplots()
    ax2.bar(df_filtrado['Country name'], df_filtrado['Logged GDP per capita'])
    plt.xticks(rotation=90)
    plt.ylabel('PIB per capita')
    st.pyplot(fig2)

st.markdown("---")

# Gráficos: dispersão e pizza
col3, col4 = st.columns(2)
with col3:
    st.subheader("🔵 Felicidade vs PIB (Dispersão Interativa)")
    fig3 = px.scatter(
        df_filtrado,
        x="Logged GDP per capita",
        y="Ladder score",
        color="Country name",
        hover_name="Country name",
        title="Felicidade x PIB per capita",
        labels={
            "Logged GDP per capita": "PIB per capita (log)",
            "Ladder score": "Índice de Felicidade"
        }
    )
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.subheader("🥧 Distribuição de Países por Região")
    regiao_count = df['Regional indicator'].value_counts()
    fig4, ax4 = plt.subplots()
    ax4.pie(regiao_count, labels=regiao_count.index, autopct='%1.1f%%')
    st.pyplot(fig4)

st.markdown("---")

# Tabela final
st.subheader("📊 Tabela de Dados da Região Selecionada")
st.dataframe(df_filtrado)
