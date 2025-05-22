codigo_app = """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Dashboard Felicidade 2021", layout="wide")

# Estilo escuro só no layout, não nos gráficos
st.markdown('''
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
''', unsafe_allow_html=True)

st.title("📊 Dashboard de Felicidade Mundial (2021)")

df = pd.read_csv("world-happiness-report-2021.csv")

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

# Gráficos agrupados em 3 colunas (fundo branco padrão)
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("**📈 Felicidade por País**")
    fig1, ax1 = plt.subplots(figsize=(3.5, 2.5))
    ax1.plot(df_filtrado['Country name'], df_filtrado['Ladder score'], color="#f7931e", marker='o', linewidth=1)
    ax1.tick_params(axis='x', labelrotation=90, labelsize=7)
    fig1.patch.set_facecolor('white')  # gráfico claro
    st.pyplot(fig1)

with col5:
    st.markdown("**💰 PIB per Capita**")
    fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))
    ax2.bar(df_filtrado['Country name'], df_filtrado['Logged GDP per capita'], color="#f7931e")
    ax2.tick_params(axis='x', labelrotation=90, labelsize=7)
    fig2.patch.set_facecolor('white')  # gráfico claro
    st.pyplot(fig2)

with col6:
    st.markdown("**🥧 Distribuição por Região**")
    regiao_count = df['Regional indicator'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(3.5, 2.5))
    ax3.pie(regiao_count, labels=regiao_count.index, autopct='%1.1f%%',
            colors=["#f7931e", "#444444", "#888888", "#CCCCCC"])
    fig3.patch.set_facecolor('white')  # gráfico claro
    st.pyplot(fig3)

st.markdown("---")

# Dispersão clara
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
"""

with open("app.py", "w") as f:
    f.write(codigo_app)

print("app.py criado com fundo escuro + gráficos claros")
