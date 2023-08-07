import streamlit as st

st.set_page_config(
    page_title = "HUB",
    layout="wide",
    initial_sidebar_state="auto"
)

st.title("Análise do número de estudantes de tecnologia (graduação), trabalhadores no setor de tecnologia e do número de doutorandos.")

st.write("Os dados apresentados neste webb app, mostram informações relativos a dados educacionais e laborais para o setor de tecnologia. Inicialmente na página 'Ensino Superior' é mostrado o número de estudantes de tecnologia à nível de graduação, baseado nos dados do censo da educação superior dos anos de 2012 a 2021 para todas as capitais do Brasil. para isso foi considerado os seguintes cursos de graduação: Análise e desenvolvimento de sistemas, Ciências da computação, Engenharia de software, Engenharia da computação, Jogos digitais, Segurança da informação, Sistemas para internet e Sistemas de informação. Todos os cursos analisados foram cursos de graduação presenciais.")


st.write("Já na página 'RAIS' é mostrado a quantidade de pessoas que trabalham como profissionais de tecnologia entre os anos de 2012 e 2021. As profissões consideradas foram as seguintes: Administrador de sistemas operacionais, Analista de testes de tecnologia da informação, Arquiteto de soluções de tecnologia da informação, Diretor de serviços de informática, Engenheiro de serviços de computação, Engenheiro de equipamentos em computação, Engenheiros de sistemas operacionais em computação, Gerente de desenvolvimento de sistemas, Gerente de produção de tecnologia da informação, Gerente de projetos de tecnologia da informação, Gerente dde segurança de tecnologia da informação, Gerente de suporte técnico de tecnologia da informação, Pesquisador de engenharia e técnologia (outras áreas da engenharia), Pesquisador em ciências da computação e informática, Professor de computação (no ensino superior), Professor de tecnologia e cálculo técnico, Programador de internet, Programador de multimidia, Programador de sistemas de informação, Técnico de apoio ao usuário de informática (HELPDESK)  e Técnico em manutenção de equipamentos de informática.")

st.write("Por fim, na página 'PNAD', mostra-se a quantidade de doutarandos por capital. Para isso buscou-se dados trimestrais na PNAD contínua relativos a educação. Para o segundo trimestre de 2019, a cidade do Rio de Janeiro (RJ) era a cidade com o maior número de doutorandos, enquanto que a cidade de Rio Branco (AC) era a capital com o menor número desses estudantes.")