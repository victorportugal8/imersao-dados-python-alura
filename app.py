import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Salários na Área de Dados", layout="wide", page_icon="📊")

# Carregamento dos dados
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Filtros
st.sidebar.header("🔍 Filtros")

anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Selecione os anos:", anos_disponiveis, default=anos_disponiveis)

senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Selecione as senioridades:", senioridades_disponiveis, default=senioridades_disponiveis)

contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Selecione os tipos de contrato:", contratos_disponiveis, default=contratos_disponiveis)

tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Selecione os tamanhos das empresas:", tamanhos_disponiveis, default=tamanhos_disponiveis)

#Filtragem dos dados no DataFrame
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# Conteúdo principal
st.title("Dashboard de Salários na Área de Dados")
st.markdown("Análise de salários na área de dados com base em diferentes critérios. Utilize os filtros à esquerda para refinar sua análise.")

# Métricas principais(KPIs)
st.subheader("Métricas gerais (Salário Anual em Dólares)")

if not df_filtrado.empty:
    media_salario = df_filtrado['usd'].mean()
    mediana_salario = df_filtrado['usd'].median()
    max_salario = df_filtrado['usd'].max()
    min_salario = df_filtrado['usd'].min()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    media_salario, mediana_salario, max_salario, min_salario, total_registros, cargo_mais_frequente = 0, 0, 0, 0, 0, "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Média Salarial", f"${media_salario:,.2f}")
col2.metric("Mediana Salarial", f"${mediana_salario:,.2f}")
col3.metric("Salário Máximo", f"${max_salario:,.2f}")
col4.metric("Salário Mínimo", f"${min_salario:,.2f}")

st.markdown("---")

# Análises Visuais utilizando Plotly
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(top_cargos, x='usd', y='cargo', orientation='h', title="Top 10 Cargos com Maior Salário Médio", labels={'usd': 'Salário Médio Anual (USD)', 'cargo': ''})
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(df_filtrado, x='usd', nbins=30, title="Distribuição dos Salários Anuais", labels={'usd': 'Salário Anual (USD)', 'count': ' ' })
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(remoto_contagem, names='tipo_trabalho', values='quantidade', title="Distribuição entre os Tipos de Trabalho", hole=0.5)
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais, locations='residencia_iso3', color='usd', color_continuous_scale='rdylgn', hover_name='residencia_iso3', title="Média Salarial de Data Scientists por País", labels={'usd': 'Salário Médio Anual (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

# Tabela detalhada de Dados
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)