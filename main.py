import streamlit as st
import pandas as pd
import plotly.express as px

#Baseado no dataset de salários de Data Science do Kaggle: https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs


st.set_page_config(page_title="Dashboard Salarial - Data Science", layout="wide")
st.title("💼 Dashboard Salarial de Profissionais de Data Science")


#Loading dos nossos dados
df = pd.read_csv("dataset/salaries.csv")


#Experience levels dos cargos
exp_dict = {
    'EN': 'Júnior',
    'MI': 'Pleno',
    'SE': 'Sênior',
    'EX': 'Executivo'
}
df['experience_level_pt'] = df['experience_level'].map(exp_dict)

#Países
country_dict = {
    'US': 'Estados Unidos',
    'GB': 'Reino Unido',
    'CA': 'Canadá',
    'IN': 'Índia',
    'DE': 'Alemanha',
    'FR': 'França',
    'ES': 'Espanha',
    'BR': 'Brasil',
    'NL': 'Holanda',
    'CH': 'Suíça',
    'AU': 'Austrália',
    'IT': 'Itália',
    'PT': 'Portugal',
    'PL': 'Polônia',
    'RO': 'Romênia'
}
df['employee_residence_pt'] = df['employee_residence'].map(country_dict).fillna(df['employee_residence'])

# Filtros laterais
#=====================================================================================================================================
with st.sidebar:
    st.header("🔎 Filtros")
    anos = st.multiselect("Ano", sorted(df['work_year'].unique()), default=df['work_year'].max())
    niveis = st.multiselect("Nível de experiência", df['experience_level_pt'].unique(), default=df['experience_level_pt'].unique())
    remoto = st.selectbox("Tipo de trabalho remoto", options=['Todos', '100% Remoto', 'Híbrido', 'Presencial'])

# Filtro de dados
filtro_df = df[df['work_year'].isin(anos)]
filtro_df = filtro_df[filtro_df['experience_level_pt'].isin(niveis)]

# Mapeia tipo remoto
if remoto != 'Todos':
    if remoto == '100% Remoto':
        filtro_df = filtro_df[filtro_df['remote_ratio'] == 100]
    elif remoto == 'Híbrido':
        filtro_df = filtro_df[(filtro_df['remote_ratio'] > 0) & (filtro_df['remote_ratio'] < 100)]
    elif remoto == 'Presencial':
        filtro_df = filtro_df[filtro_df['remote_ratio'] == 0]

# KPIs principais
col1, col2, col3 = st.columns(3)
col1.metric("Salário Médio (USD)", f"$ {filtro_df['salary_in_usd'].mean():,.0f}")
col2.metric("Mediana Salarial", f"$ {filtro_df['salary_in_usd'].median():,.0f}")
col3.metric("Nº de Registros", f"{len(filtro_df)}")

st.markdown("---")

#=====================================================================================================================================


# Gráfico 1: Salário por cargo
fig1 = px.box(filtro_df, x="job_title", y="salary_in_usd", color="experience_level_pt",
              title="Distribuição Salarial por Cargo", labels={"salary_in_usd": "Salário (USD)", "job_title": "Cargo"})
fig1.update_layout(xaxis_tickangle=-45, height=500)
st.plotly_chart(fig1, use_container_width=True)



# Gráfico 2: Salário médio por país
sal_pais = filtro_df.groupby("employee_residence_pt")["salary_in_usd"].mean().sort_values(ascending=False).head(15).reset_index()
fig2 = px.bar(sal_pais, x="employee_residence_pt", y="salary_in_usd",
              title="Top 15 Países com Maior Salário Médio",
              labels={"employee_residence_pt": "País", "salary_in_usd": "Salário Médio (USD)"})
st.plotly_chart(fig2, use_container_width=True)



# Gráfico 3: Evolução temporal 
fig3 = px.line(filtro_df.groupby("work_year")["salary_in_usd"].mean().reset_index(),
               x="work_year", y="salary_in_usd",
               title="Evolução do Salário Médio por Ano",
               labels={"work_year": "Ano", "salary_in_usd": "Salário Médio (USD)"})
st.plotly_chart(fig3, use_container_width=True)



#Gráfico 4: Salário por tamanho da empresa (aqui a gente poderia mehlhorar, mas vamos deixar assim por enquanto)
size_dict = {'S': 'Pequena', 'M': 'Média', 'L': 'Grande'}
filtro_df['company_size_pt'] = filtro_df['company_size'].map(size_dict)
sal_size = filtro_df.groupby("company_size_pt")["salary_in_usd"].mean().reset_index()
fig4 = px.bar(sal_size, x="company_size_pt", y="salary_in_usd",
              title="Salário Médio por Tamanho da Empresa",
              labels={"company_size_pt": "Tamanho da Empresa", "salary_in_usd": "Salário Médio (USD)"})
st.plotly_chart(fig4, use_container_width=True)



st.markdown("---")
st.caption("Fonte: Kaggle - Data Science Salaries Dataset | Criado com Streamlit e Plotly")
st.caption("Reproduced for @usmarcv on GitHub")
