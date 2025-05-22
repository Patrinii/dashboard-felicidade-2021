
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Dashboard Felicidade 2021", layout="wide")
st.title("🌍 Dashboard - Relatório Mundial da Felicidade (2021)")

# Carrega o CSV
df = pd.read_csv("world-happiness-report-2021.csv")

# Filtro por região
regioes = df['Regional indicator'].unique()
regiao_selecionada = st.selectbox("Selecione uma região:", regioes)
df_filtrado = df[df['Regional indicator'] == regiao_selecionada]

# Tabela de dados
st.markdown("### 📊 Dados da Região Selecionada")
st.dataframe(df_filtrado)

# Gráficos lado a lado: Linha e Barras
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Gráfico de Linha - Felicidade")
    fig1, ax1 = plt.subplots()
    ax1.plot(df_filtrado['Country name'], df_filtrado['Ladder score'], marker='o')
    plt.xticks(rotation=90)
    plt.ylabel('Ladder Score')
    st.pyplot(fig1)

with col2:
    st.subheader("📊 Gráfico de Barras - PIB per capita")
    fig2, ax2 = plt.subplots()
    ax2.bar(df_filtrado['Country name'], df_filtrado['Logged GDP per capita'])
    plt.xticks(rotation=90)
    plt.ylabel('PIB per capita')
    st.pyplot(fig2)

# Gráfico dispersão interativo em tela cheia
st.subheader("🔵 Dispersão Interativa - Felicidade x PIB")
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

# Gráfico de pizza + observações
col3, col4 = st.columns(2)

with col3:
    st.subheader("🥧 Gráfico de Pizza - Países por Região")
    regiao_count = df['Regional indicator'].value_counts()
    fig4, ax4 = plt.subplots()
    ax4.pie(regiao_count, labels=regiao_count.index, autopct='%1.1f%%')
    st.pyplot(fig4)

with col4:
    st.subheader("ℹ️ Observações")
    st.markdown("""
    - Este painel permite visualizar dados da felicidade em 2021.
    - Use o filtro acima para selecionar uma região.
    - Os gráficos estão organizados em colunas para facilitar a comparação.
    """)
