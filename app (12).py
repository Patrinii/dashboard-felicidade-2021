
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Fundo escuro no layout
st.set_page_config(page_title="Dashboard Felicidade 2021", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #111111;
            color: #FFFFFF;
        }
        h1, h2, h3, h4 {
            color: #f7931e;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .element-container {
            background-color: transparent !important;
        }
        .stPlotlyChart > div {
            background-color: white !important;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard de Felicidade Mundial (2021)")

df = pd.read_csv("world-happiness-report-2021.csv")
regioes = df['Regional indicator'].unique()
regiao_selecionada = st.selectbox("🌍 Selecione uma região:", regioes)
df_filtrado = df[df['Regional indicator'] == regiao_selecionada]

# KPIs com cores diferentes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='background-color:#1e3a8a; padding:15px; border-radius:10px; text-align:center; color:white'>
            <h4>Média de Felicidade</h4>
            <h2>{:.2f}</h2>
        </div>
    """.format(df_filtrado['Ladder score'].mean()), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='background-color:#facc15; padding:15px; border-radius:10px; text-align:center; color:black'>
            <h4>PIB Médio (log)</h4>
            <h2>{:.2f}</h2>
        </div>
    """.format(df_filtrado['Logged GDP per capita'].mean()), unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='background-color:#22c55e; padding:15px; border-radius:10px; text-align:center; color:white'>
            <h4>Total de Países</h4>
            <h2>{}</h2>
        </div>
    """.format(len(df_filtrado)), unsafe_allow_html=True)

st.markdown("---")

# Gráficos agrupados
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("**📈 Felicidade por País**")
    fig1, ax1 = plt.subplots(figsize=(3.5, 2.5))
    ax1.plot(df_filtrado['Country name'], df_filtrado['Ladder score'], color="#f7931e", marker='o', linewidth=1)
    ax1.tick_params(axis='x', labelrotation=90, labelsize=7)
    fig1.patch.set_facecolor("white")
    ax1.set_facecolor("white")
    st.pyplot(fig1)

with col5:
    st.markdown("**💰 PIB per Capita**")
    fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))
    ax2.bar(df_filtrado['Country name'], df_filtrado['Logged GDP per capita'], color="#f7931e")
    ax2.tick_params(axis='x', labelrotation=90, labelsize=7)
    fig2.patch.set_facecolor("white")
    ax2.set_facecolor("white")
    st.pyplot(fig2)

with col6:
    st.markdown("**🥧 Distribuição por Região**")
    regiao_count = df['Regional indicator'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(3.5, 2.5))
    fig3.patch.set_facecolor("white")
    ax3.set_facecolor("white")
    ax3.pie(regiao_count, labels=regiao_count.index, autopct='%1.1f%%',
            colors=["#f7931e", "#444444", "#888888", "#CCCCCC"])
    st.pyplot(fig3)

st.markdown("---")

# Dispersão
st.markdown("**🔵 Felicidade x PIB per Capita**")
fig4 = px.scatter(
    df_filtrado,
    x="Logged GDP per capita",
    y="Ladder score",
    color="Country name",
    hover_name="Country name",
    labels={
        "Logged GDP per capita": "PIB per capita (log)",
        "Ladder score": "Felicidade"
    },
    height=320,
    width=950,
    color_discrete_sequence=px.colors.sequential.Oranges
)
st.plotly_chart(fig4, use_container_width=True)

# Tabela
st.subheader("📋 Tabela de Dados da Região Selecionada")
st.dataframe(df_filtrado.style.background_gradient(cmap='Oranges'))
