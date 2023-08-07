import pandas as pd
import streamlit as st
import os

import plotly.express as px
import numpy as np
import plotly as plt

import plotly.graph_objects as go

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

#-------------------------------------------------------------------------------------------------------------
# Manipulação e importação dos dados
#-------------------------------------------------------------------------------------------------------------

# Obter o caminho absoluto para a pasta "dados"
path = os.path.abspath('dados')

# Nome do arquivo Excel
file_name = 'rais.xlsx'

# Combinar o caminho com o nome do arquivo para obter o caminho completo
excel_file = os.path.join(path, file_name)

# Ler o Excel em um DataFrame
rais = pd.read_excel(excel_file)


st.title("Relação Anual de Informações Sociais - RAIS")

st.write("Conforme é mostrado no próprio site do Ministério do Trabalho e Previdência (MTE): 'A Relação Anual de Informações Sociais (RAIS) tem por objetivo o suprimento às necessidades de controle da atividade trabalhista no país, para identificação dos trabalhadores com direito ao recebimento do Abono Salarial. Outras funções são o provimento de dados para a elaboração de estatísticas do trabalho e a disponibilização de informações do mercado de trabalho às entidades governamentais.'")

st.header("Número de trabalhadores formais no setor de tecnologia por capital. 2012-2021")

st.write("A figura abaixo mostra a quantidade de trabalhadores formais que atuam no setor de sectnologia por capital entre os anos de 2012 e 2021. Foram consideradas as seguintes profissões: Administrador de sistemas operacionais, Analista de testes de tecnologia da informação, Arquiteto de soluções de tecnologia da informação, Diretor de serviços de informática, Engenheiro de serviços de computação, Engenheiro de equipamentos em computação, Engenheiros de sistemas operacionais em computação, Gerente de desenvolvimento de sistemas, Gerente de produção de tecnologia da informação, Gerente de projetos de tecnologia da informação, Gerente dde segurança de tecnologia da informação, Gerente de suporte técnico de tecnologia da informação, Pesquisador de engenharia e técnologia (outras áreas da engenharia), Pesquisador em ciências da computação e informática, Professor de computação (no ensino superior), Professor de tecnologia e cálculo técnico, Programador de internet, Programador de multimidia, Programador de sistemas de informação, Técnico de apoio ao usuário de informática (HELPDESK)  e Técnico em manutenção de equipamentos de informática.")

# Cria uma variável, verique todos os valores únicos e crie uma lista com esses valores únicos
clist = rais["cidade"].unique().tolist()
capitais = st.multiselect("Selecione uma ou mais capitais", clist)
st.write("Você selecionou: {}".format(", ".join(capitais)))
dfs = {capital: rais[rais["cidade"] == capital] for capital in capitais}
fig = go.Figure()
for capital, rais in dfs.items():
    fig = fig.add_trace(go.Scatter(mode="lines+markers", x=rais["ano"], y=rais["total"], name=capital,text=['total']))
    fig.update_layout(
    title_text='', 
    yaxis_title = "Taxa de trabalhadores",
    xaxis_title = "Ano")

st.plotly_chart(fig, use_container_width=True)

st.header("Quantidade de profissionais por região")

st.write("Abaixo é mostrado a quantidade total de trabalhadores formais na área de tecnologia por região (apenas as capitais), dados as profissões mencionados acima. Como é visto abaixo, As capitais da região sudeste concentram uma grande quantidade desses profisionais.")

# Importando os dados
dados_regioes = pd.read_excel(excel_file)

# Média por região e por ano
dados_regioes = pd.DataFrame(dados_regioes.groupby(["regiao","ano"])["total"].sum())

# organizando as colunas-índices
dados_regioes = dados_regioes.reset_index(level=0)
dados_regioes = dados_regioes.reset_index(level=0)

# Arredondando valores
dados_regioes['total'] = dados_regioes['total'].round(0)

# Plotando a figura
fig_regioes = px.line(dados_regioes, x='ano', y="total", title='', color='regiao',
                      symbol = 'regiao',
                      labels={
                          "ano": "Ano",
                          "total": "Total de trabalhadores",
                          "regiao":"Região"
   })

st.plotly_chart(fig_regioes, use_container_width=True)

st.header('Profissionais por capital - 2021')

st.write("Por fim, verifica-se como estão distribuidos os tipos de profissionais de tecnologia por capital para o ano de 2021. As profissões são definidas pela Classificação Brasileira de Ocupações (CBO) de 2002 (*).")

# Importando os dados
rais2021 = pd.read_excel(excel_file)

# removendo os dados faltantes
rais2021 = rais2021.dropna()

# Transformando de object para float
rais2021['Aracaju - SE'] = rais2021['Aracaju - SE'].astype(float)
rais2021['Belo Horizonte - MG'] = rais2021['Belo Horizonte - MG'].astype(float)

# Mantendo palavras chaves das profissões de interesse
rais2021 = rais2021[rais2021['CBO Ocupação 2002'].str.contains("TECNOLOGIA")
         | rais2021['CBO Ocupação 2002'].str.contains("SISTEMA")
         | rais2021['CBO Ocupação 2002'].str.contains("COMPUTACAO")
         | rais2021['CBO Ocupação 2002'].str.contains("INFORMATICA")
         | rais2021['CBO Ocupação 2002'].str.contains("PROGRAMADOR")]

# removendo profissões de não interesse
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("ENCARREGADO DE MANUTENCAO MECANICA DE SISTEMAS OPERACIONAIS")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("TECNÓLOGO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("ELETROELETRONICOS")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("MECANICO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("OPERADOR")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("MONTADOR")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("IRRIGACAO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("BIOTECNOLOGIA")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("TECNICO DE APOIO AO USUARIO DE INFORMATICA (HELPDESK)")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("TECNICO DE MANUTENCAO DE SISTEMAS E INSTRUMENTOS")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("PROJETISTA DE SISTEMAS DE AUDIO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("TELEVISAO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("ANALISTA DE SISTEMAS DE AUTOMACAO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("MONITOR")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("PROGRAMADOR VISUAL GRAFICO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("PROGRAMADOR DE MAQUINAS - FERRAMENTA COM COMANDO NUMERICO")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("TECNICO DE SISTEMAS AUDIOVISUAIS")]
rais2021 = rais2021[~rais2021['CBO Ocupação 2002'].str.contains("INSTALADOR DE SISTEMAS FOTOVOLTAICOS")]


rais2021['CBO Ocupação 2002'] = [x.replace('DIRETOR DE SERVICOS DE INFORMATICA', 'Diretor de serv. de informática') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('GERENTE DE DESENVOLVIMENTO DE SISTEMAS', 'Gerente de desenv. de sist.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('GERENTE DE PRODUCAO DE TECNOLOGIA DA INFORMACAO', 'Gerente de produç. de tec. da informac.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('GERENTE DE PROJETOS DE TECNOLOGIA DA INFORMACAO', 'Gerente de proj. de tec. da informac.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('GERENTE DE SEGURANCA DE TECNOLOGIA DA INFORMACAO', 'Gerente de seg. de tec. da informac.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('GERENTE DE SUPORTE TECNICO DE TECNOLOGIA DA INFORMACAO', 'Gerente de supor. de tecnico de tec. da informac.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('GERENTE DE SUPORTE TECNICO DE TECNOLOGIA DA INFORMACAO', 'Gerente de supor. de tecnico de tec. da informac.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PESQUISADOR EM CIENCIAS DA COMPUTACAO E INFORMATICA', 'Pesquisador em ciênc. da comput. e informat.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PESQUISADOR DE ENGENHARIA E TECNOLOGIA (OUTRAS AREAS DA ENGENHARIA)', 'Pesquisador de eng. e tec. (**)') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('ENGENHEIRO DE APLICATIVOS EM COMPUTACAO', 'Engenheiro de aplic. em comput.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('ENGENHEIRO DE EQUIPAMENTOS EM COMPUTACAO', 'Engenheiro de equip. em comput.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('ENGENHEIROS DE SISTEMAS OPERACIONAIS EM COMPUTACAO', 'Engenheiros de sist. operac. em comput.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('ADMINISTRADOR DE SISTEMAS OPERACIONAIS', 'Administrador de sist. operac.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('ANALISTA DE DESENVOLVIMENTO DE SISTEMAS', 'Analista de desenv. de sist.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('ARQUITETO DE SOLUÇÕES DE TECNOLOGIA DA INFORMAÇÃO', 'Arquiteto de sol. de tec. da info.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('ANALISTA DE TESTES DE TECNOLOGIA DA INFORMAÇÃO', 'Analista de testes de tec. da info.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PROFESSOR DE TECNOLOGIA E CALCULO TECNICO', 'Professor de tec. e calc. técnico') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PROFESSOR DE COMPUTACAO (NO ENSINO SUPERIOR)', 'Professor de compt. (Ensino Sup.)') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('TECNICO EM MANUTENCAO DE EQUIPAMENTOS DE INFORMATICA', 'técnico em manut. de equipa. de informática') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PROGRAMADOR DE INTERNET', 'Programador de internet') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PROGRAMADOR DE SISTEMAS DE INFORMACAO', 'Programador de sist. de info.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PROGRAMADOR DE MULTIMIDIA', 'Programador de multimidia.') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('TECNICO DE APOIO AO USUARIO DE INFORMATICA (HELPDESK)', 'Técnico de apoio ao usu. de informática (Helpdesk)') for x in rais2021['CBO Ocupação 2002']]
rais2021['CBO Ocupação 2002'] = [x.replace('PROFESSOR DE TECNOLOGIA E CALCULO TECNICO', 'Técnico de apoio ao usu. de informática (Helpdesk)') for x in rais2021['CBO Ocupação 2002']]

# Criando uma caixa de seleção
escolha = st.selectbox(
    'Qual capital você deseja visualizar',
    ('Selecione uma capital', 'Aracaju', 'Belo Horizonte', 'Belém', 'Boa Vista', 'Brasília', 'Campo Grande', 'Cuiabá', 'Curitiba', 'Florianópolis', 'Fortaleza',
                            'Goiânia', 'João Pessoa', 'Macapá', 'Maceió', 'Manaus', 'Natal', 'Palmas', 'Porto Alegre', 'Porto Velho', 'Recife', 'Rio Branco',
                            'Rio de Janeiro', 'Salvador', 'São Luiz', 'São Paulo', 'Teresina', 'Vitória'))

# aracajú
if escolha == 'Aracaju':
    # Aracaju
    fig_aracaju = px.bar(rais2021, x='Aracaju - SE', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_aracaju.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                font=dict(size=12))
    st.plotly_chart(fig_aracaju, use_container_width=True)
    
# Belo Horizonte
if escolha == 'Belo Horizonte': 
    fig_bh = px.bar(rais2021, x='Belo Horizonte - MG', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_bh.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_bh, use_container_width=True)

# Belém
if escolha == 'Belém':
    fig_belem = px.bar(rais2021, x='Belém - PA', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_belem.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_belem, use_container_width=True)
    
# Boa Vista
if escolha == 'Boa Vista':
    fig_bv = px.bar(rais2021, x='Boa Vista - RR', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_bv.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_bv, use_container_width=True)

# Brasília
if escolha == 'Brasília':
    fig_brasilia = px.bar(rais2021, x='Brasília - DF', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_brasilia.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_brasilia, use_container_width=True)

# Campo Grande
if escolha == 'Campo Grande':
    fig_cg = px.bar(rais2021, x='Campo Grande - MS', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_cg.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_cg, use_container_width=True)
    
# Cuiabá
if escolha == 'Cuiabá':
    fig_cuiaba = px.bar(rais2021, x = 'Cuiabá - MT', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_cuiaba.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_cuiaba, use_container_width=True)
    
# Curitiba
if escolha == 'Curitiba':
    fig_curitiba = px.bar(rais2021, x = 'Curitiba - PR', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_curitiba.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_curitiba, use_container_width=True)
    
# Florianópolis
if escolha == 'Florianópolis':
    fig_florianopolis = px.bar(rais2021, x = 'Florianópolis - SC', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_florianopolis.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_florianopolis, use_container_width=True)

# Fortaleza
if escolha == 'Fortaleza':
    fig_fortaleza = px.bar(rais2021, x = 'Fortaleza - CE', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_fortaleza.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_fortaleza, use_container_width=True)
    
# Goiânia
if escolha == 'Goiânia':
    fig_goiania = px.bar(rais2021, x = 'Goiânia - GO', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_goiania.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_goiania, use_container_width=True)

# João Pessoa
if escolha == 'João Pessoa':
    fig_jp = px.bar(rais2021, x = 'João Pessoa - PB', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_jp.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_jp, use_container_width=True)
    
# Macapá
if escolha == 'Macapá':
    fig_macapa = px.bar(rais2021, x = 'Macapá - AP', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_macapa.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_macapa, use_container_width=True)
    
# Maceió
if escolha == 'Maceió':
    fig_maceio = px.bar(rais2021, x = 'Maceió - AL', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_maceio.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_maceio, use_container_width=True)

# Manaus
if escolha == 'Manaus':
    fig_manaus = px.bar(rais2021, x = 'Manaus - AM', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_manaus.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_manaus, use_container_width=True)
    
# Natal
if escolha == 'Natal':
    fig_natal = px.bar(rais2021, x = 'Natal - RN', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_natal.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_natal, use_container_width=True)

# Palmas
if escolha == 'Palmas':
    fig_palmas = px.bar(rais2021, x = 'Palmas - TO', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_palmas.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_palmas, use_container_width=True)

# Porto Alegre
if escolha == 'Porto Alegre':
    fig_poa = px.bar(rais2021, x = 'Porto Alegre - RS', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_poa.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_poa, use_container_width=True)

# Porto Velho
if escolha == 'Porto Velho':
    fig_pv = px.bar(rais2021, x = 'Porto Velho - RO', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_pv.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_pv, use_container_width=True)

# Recife
if escolha == 'Recife':
    fig_recife = px.bar(rais2021, x = 'Recife - PE', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_recife.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_recife, use_container_width=True)

# Rio Branco
if escolha == 'Rio Branco':
    fig_rb = px.bar(rais2021, x = 'Rio Branco - AC', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_rb.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_rb, use_container_width=True)
    
# Rio de Janeiro
if escolha == 'Rio de Janeiro':
    fig_rj = px.bar(rais2021, x = 'Rio de Janeiro - RJ', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_rj.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_rj, use_container_width=True)

# Salvador
if escolha == 'Salvador':
    fig_salvador = px.bar(rais2021, x = 'Salvador - BA', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_salvador.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_salvador, use_container_width=True)

# São Luiz
if escolha == 'São Luiz':
    fig_sl = px.bar(rais2021, x = 'São Luiz - MA', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_sl.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_sl, use_container_width=True)

# São Paulo
if escolha == 'São Paulo':
    fig_sp = px.bar(rais2021, x = 'São Paulo - SP', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_sp.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_sp, use_container_width=True)

# Teresina
if escolha == 'Teresina':
    fig_teresina = px.bar(rais2021, x = 'Teresina - PI', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_teresina.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_teresina, use_container_width=True)

# Vitória
if escolha == 'Vitória':
    fig_vitoria = px.bar(rais2021, x = 'Vitória - ES', y='CBO Ocupação 2002', text_auto=True, orientation='h', height=800)
    fig_vitoria.update_layout(barmode='stack', yaxis={'categoryorder': 'total ascending'},
                                                    font=dict(size=12))
    st.plotly_chart(fig_vitoria, use_container_width=True)

st.caption('(*)  Nome das profissões abreviadas para fins de visualização gráfica.')
st.caption('(**)  Nome completo da profissão: PESQUISADOR DE ENGENHARIA E TECNOLOGIA (OUTRAS AREAS DA ENGENHARIA).')
