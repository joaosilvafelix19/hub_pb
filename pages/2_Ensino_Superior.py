import pandas as pd
import streamlit as st
import os
import plotly.express as px
import numpy as np
import plotly as plt
import json
from urllib.request import urlopen
import plotly.graph_objects as go

from IPython import display

#-------------------------------------------------------------------------------------------------------------
# Manipulação e importação dos dados
#-------------------------------------------------------------------------------------------------------------

# Obter o caminho absoluto para a pasta "dados"
path = os.path.abspath('dados')

# Nome do arquivo Excel
file_name = 'ens_sup.xlsx'

# Combinar o caminho com o nome do arquivo para obter o caminho completo
excel_file = os.path.join(path, file_name)

# Ler o Excel em um DataFrame
ens_sup = pd.read_excel(excel_file)

# Arredondando
ens_sup['taxa'] = ens_sup['taxa'].round(0)
dados_regioes = ens_sup

# DataFrame com a logintude dos estados
soybean = pd.read_csv('https://raw.githubusercontent.com/nayanemaia/Dataset_Soja/main/soja%20sidra.csv')
soybean.rename({'Estado': 'estado'}, axis=1, inplace=True)

# Formato do Brasil
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
 Brazil = json.load(response) 
 
 
state_id_map = {}
for feature in Brazil ['features']:
    feature['id'] = feature['properties']['name']
    state_id_map[feature['properties']['sigla']] = feature['id']
    
# Inserindo os dados de latitude e longitude
df_map = pd.merge(left=ens_sup, right=soybean, on='estado', how='left')

# Dropando colunas desnecessárias
df_map.drop(['ano_y', 'Produção', 'Unnamed: 5'], axis=1, inplace=True)

# renomeando coluna
df_map.rename({'ano_x': 'ano'}, axis=1, inplace=True)

#-------------------------------------------------------------------------------------------------------------
# Página
#-------------------------------------------------------------------------------------------------------------
st.title("Censo da Educação Superior - 2012 a 2021")
st.write("O Censo da Educação Superior é realizado anualmente pelo INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira), e tem como objetivo levantar estatísticas relativas aos cursos de graduação, cursos sequênciais de formação especifíca, estudantes e docentes. Abaixo será mostrado algumas informações sobre a quantidade (taxa) de estudantes a cada 100 000 habitantes para as capitais brasileiras e para as 5 regiões nacionais, entre os anos de 2012 e 2015.")

st.write("Os cursos levados em consideração foram: Análise e desenvolvimento de sistemas, Ciências da computação, Engenharia de software, Engenharia da computação, Jogos digitais, Segurança da informação, Sistemas para internet e Sistemas de informação. Todos os cursos analisados foram cursos de graduação presenciais.")

st.header("Taxa a cada 100 mil habitantes por capital")

st.write("Abaixo é mostrado a evolução do número de estudantes a cada 100 000 habitantes entre os anos de 2012 e 2021. No Ano de 2021 a capital com a maior taxa foi Vitória-ES com uma taxa 389,13, seguido por Recife-PE com uma taxa de 362,09, já a capital com a menor taxa foi Natal-RN com uma taxa de 91. A capital da Paraíba, João Pessoa, tinha em 2021 a 6° maior taxa, com 252,48 estudantes de tecnologia a cada 100 000 habitantes.")

Opção = st.radio("Escolha uma opção para visualização dos dados",
                 ('Linha', 'Mapa'))

if Opção == "Linha":
    clist = ens_sup["capital"].unique().tolist()
    capitais = st.multiselect("Selecione uma ou mais capitais", clist, default="João Pessoa")
    st.write("Você selecionou: {}".format(", ".join(capitais)))
    dfs = {capital: ens_sup[ens_sup["capital"] == capital] for capital in capitais}
    fig = go.Figure()
    for capital, ens_sup in dfs.items():
        fig = fig.add_trace(go.Scatter(mode="lines+markers", x=ens_sup["ano"], y=ens_sup["taxa"], name=capital,text=['taxa']))
        fig.update_layout(
        title_text='', 
        yaxis_title = "Taxa 100.000 habitantes",
        xaxis_title = "Ano"
        )
    st.plotly_chart(fig, use_container_width=True)
    
if Opção == "Mapa":
    mapa_taxa = px.choropleth(
        df_map, 
        locations = 'estado', 
        geojson = Brazil, 
        color = "taxa", 
        color_continuous_scale="Greens",
        hover_name = 'estado', 
        hover_data =["taxa","Longitude","Latitude"],
        title = "Estudantes de tecnologia a cada 100 000 habitantes por capital", 
        animation_frame = 'ano',
         labels={
                     "taxa": "Taxa"
                 })
    mapa_taxa.update_geos(fitbounds = "locations", visible = False)
    st.plotly_chart(mapa_taxa, use_container_width=True)

st.header("Taxa a cada 100 mil habitantes por região")

st.write("Abaixo mostra-se como evoluiu a taxa de estudantes de tecnologia para cada região do país (considerando apenas as capitais.) ")

# Média por região e por ano
regioes = pd.DataFrame(dados_regioes.groupby(["regiao","ano"])["taxa"].mean())

# Arredondando valores
regioes['taxa'] = regioes['taxa'].round(0)

# Fazendo as colunas indíces em coluna variável
regioes = regioes.reset_index(level=0)
regioes = regioes.reset_index(level=0)

fig_regioes = px.line(regioes, x='ano', y="taxa", title='', color='regiao', 
              symbol="regiao",
              text="taxa",
              labels={
                     "ano": "Ano",
                     "taxa": "Taxa 100.000 habitantes",
                     "regiao":"Região"
                 })
st.plotly_chart(fig_regioes, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    tab_regiao = dados_regioes.groupby("regiao")["taxa"].mean().reset_index()
    tab_regiao = tab_regiao.sort_values(by=['taxa'], ascending=False)
    tab_regiao['taxa'] = tab_regiao['taxa'].round(2)
    tab_regiao.rename({'regiao': 'Região', 'taxa':'Taxa'}, axis=1, inplace=True)
    
    # Converta a Series tab_regiao para um DataFrame
    df_tab_regiao = pd.DataFrame(tab_regiao)
    
    # Criação da tabela HTML
    html_table = df_tab_regiao.to_html(index=False)
    display(HTML(html_table))
    
with col2:
    st.write("Ao lado, é mostrado a taxa de estudantes de tecnologia para as 5 grandes regiões brasileiras, as taxas ao lado leva em consideração todo o período de análise (2012-2021). Como é visto, as região sul e sudeste apresentam as maiores taxas, a região norte é aquela com a menor taxa do país.")
    

st.write("Por fim, mostra-se a variação na taxa a cada 100 000 habitantes para estudantes dos cursos de tecnologia selecionados entres os anos de 2021 e 2020. Na cidade de João Pessoa, em 2021, existiam 252 estudantes de tecnologia a cada 100 000 habitantes, isto representa um avanço de 17 estudantes em relação ao ano de 2020. Já no Nordeste (incluindo João Pessoa), a taxa em 2021 foi de 181 estudantes, e no Brasil, a taxa foi de 195,96.")

cola, colb, colc = st.columns(3)
cola.metric(label="João Pessoa", value=252, delta=17) 
colb.metric(label="Nordeste", value=181, delta=6)
colc.metric(label="Brasil", value=195.96, delta=1.59)


