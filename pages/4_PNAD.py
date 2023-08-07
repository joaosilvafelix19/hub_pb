import pandas as pd
import streamlit as st
import os

import plotly.express as px
import numpy as np
import plotly as plt

import plotly.graph_objects as go

#-------------------------------------------------------------------------------------------------------------
# Manipulação e importação dos dados
#-------------------------------------------------------------------------------------------------------------

# Definindo diretório
#os.chdir("C:\\Users\\joaos\\Documents\\MeusProjetos\\hub_pb\\dados")
# Obter o caminho absoluto para a pasta "dados"
path = os.path.abspath('dados')

# Nome do arquivo Excel
file_name = 'pnad.xlsx'

# Combinar o caminho com o nome do arquivo para obter o caminho completo
excel_file = os.path.join(path, file_name)

# Ler o Excel em um DataFrame
rais = pd.read_excel(excel_file)

# Importando os dados
pnad = pd.read_excel(excel_file)
pnad1 = pnad

# Dropando colunas
pnad = pnad.drop(['Unnamed: 0'], axis=1)

# Renomeando colunas
pnad.rename(columns={"Ano": "ano", "Trimestre":"trimestre", "UF":"uf",
                     "Capital":"capital", "V1023":"tipo_area", "V1028":"peso",
                     "V1029":"populacao", "V3003A":"curso"}, inplace=True)

# Transformando int para string
pnad['ano'] = pnad['ano'].astype(str)
pnad['trimestre'] = pnad['trimestre'].astype(str)

# Criando uma coluna ano_tri
pnad["ano_tri"] = pnad['ano'] + '.' + pnad['trimestre']

# transformando a coluna ano_tri para float
pnad['ano_tri'] = pnad['ano_tri'].astype(float)

# Parte 2
pnad_pop = pnad[['uf', 'populacao', 'ano', 'trimestre']]

# Transformando int para string
pnad_pop['ano'] = pnad_pop['ano'].astype(str)
pnad_pop['trimestre'] = pnad_pop['trimestre'].astype(str)

# Criando uma coluna ano_tri
pnad_pop["ano_tri"] = pnad_pop['ano'] + '.' + pnad_pop['trimestre']

# transformando a coluna ano_tri para float
pnad_pop['ano_tri'] = pnad_pop['ano_tri'].astype(float)

# Organizando de forma ascendente uf e ano_trimestre
pnad_pop = pnad_pop.sort_values(by=['uf', 'ano_tri'], ascending=True)

# Parte 3

# Soma agrupada por ano, trimestre e capital
pnad = pnad.groupby(["ano_tri","uf"])["peso"].sum()

# Transformando index em coluna
pnad = pnad.reset_index(level=0)
pnad = pnad.reset_index(level=0)

# Organizando de forma ascendente uf e ano_trimestre
pnad = pnad.sort_values(by=['uf', 'ano_tri'], ascending=True)

# Arredondando a coluna peso
pnad['peso'] = pnad['peso'].round(decimals = 0)

# Renomeando a coluna peso para total
pnad.rename(columns={"peso": "total"}, inplace=True)

# Parte 4

# PNAD total
pnadt = pd.merge(pnad, pnad_pop,  how='left', left_on=['uf','ano_tri'], right_on = ['uf','ano_tri'])

# mantendo apenas as primeiras repetições
pnadt = pnadt.drop_duplicates(keep='first')

# Criando a coluna taxa
pnadt['taxa'] = (pnadt['total']/pnadt['populacao'])*100000


#-------------------------------------------------------------------------------------------------------------
# Página
#-------------------------------------------------------------------------------------------------------------
st.title("PNAD Contínua - Pesquisa Nacional por Amostra de Domicílios")

st.write('Nesta seção, será apresentado a quantidade de pessoas que frequentavam o curso de doutorado por trimestre entre os anos de 2016 e 2019 para todos as capitais do Brasil. Note que abaixo, ao selecionar a região de interesse irá aparecer o nome dos estados, entretanto, apenas as capitais foram analisadas, logo, quando seleciona-se, por exemplo, Paraíba, estamos analisando apenas os dados de sua capital, João Pessoa.')

st.header("Evolução da taxa de estudantes - 100 000 habitantes")

clist = pnadt["uf"].unique().tolist()
capitais = st.multiselect("Selecione uma ou mais capitais", clist, default="Paraíba")
st.write("Você selecionou: {}".format(", ".join(capitais)))
dfs = {capital: pnadt[pnadt["uf"] == capital] for capital in capitais}
fig = go.Figure()
for capital, pnadt in dfs.items():
    fig = fig.add_trace(go.Scatter(mode="lines+markers", x=pnadt["ano_tri"], y=pnadt["taxa"], name=capital,text=['taxa']))
    fig.update_layout(
    title_text='', 
    yaxis_title = "Taxa estudantes doutorado",
    xaxis_title = "Ano e trimestre",
    font = dict(size = 15),
    xaxis = dict(
      tickmode = 'linear',
      tick0 = 1,
      dtick = 1
   )
    )

st.plotly_chart(fig, use_container_width=True)

st.header('Taxa de doutorandos no segundo trimestre de 2019 a cada 100 000 habitantes')

st.write('Dados não disponíveis para Mato Grosso e Piauí, para o segundo semestre de 2019')

pnad1 = pd.read_excel(excel_file)

pnad1 = pnad1.drop(['Unnamed: 0'], axis=1)
pnad1.rename(columns={"Ano": "ano", "Trimestre":"trimestre", "UF":"uf",
                     "Capital":"capital", "V1023":"tipo_area", "V1028":"peso",
                     "V1029":"populacao", "V3003A":"curso"}, inplace=True)
pnad1['ano'] = pnad1['ano'].astype(str)
pnad1['trimestre'] = pnad1['trimestre'].astype(str)
pnad1["ano_tri"] = pnad1['ano'] + '.' + pnad1['trimestre']
pnad1['ano_tri'] = pnad1['ano_tri'].astype(float)

# Parte 2
pnad1_pop = pnad1[['uf', 'populacao', 'ano', 'trimestre']]
pnad1_pop['ano'] = pnad1_pop['ano'].astype(str)
pnad1_pop['trimestre'] = pnad1_pop['trimestre'].astype(str)
pnad1_pop["ano_tri"] = pnad1_pop['ano'] + '.' + pnad1_pop['trimestre']
pnad1_pop['ano_tri'] = pnad1_pop['ano_tri'].astype(float)
pnad1_pop = pnad1_pop.sort_values(by=['uf', 'ano_tri'], ascending=True)

# Parte 3
pnad1 = pnad1.groupby(["ano_tri","uf"])["peso"].sum()
pnad1 = pnad1.reset_index(level=0)
pnad1 = pnad1.reset_index(level=0)
pnad1 = pnad1.sort_values(by=['uf', 'ano_tri'], ascending=True)
pnad1['peso'] = pnad1['peso'].round(decimals = 0)
pnad1.rename(columns={"peso": "total"}, inplace=True)

# Parte 4
pnadt = pd.merge(pnad1, pnad_pop,  how='left', left_on=['uf','ano_tri'], right_on = ['uf','ano_tri'])
pnadt = pnadt.drop_duplicates(keep='first')
pnadt['taxa'] = (pnadt['total']/pnadt['populacao'])*100000

# Parte 5
nd = pnadt[(pnadt.ano_tri == 2019.2)]
nd = nd[['uf', 'taxa']]
nd.rename(columns={'uf':'Estado/Capital', 'taxa':'Taxa 100 000 Habitantes'}, inplace=True)
nd = nd.sort_values(by=['Taxa 100 000 Habitantes'], ascending=False)
nd['Taxa 100 000 Habitantes'] = nd['Taxa 100 000 Habitantes'].round(0)

# Parte 6
st.dataframe(nd)