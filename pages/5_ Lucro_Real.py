import streamlit as st
import plotly.express as px


st.title("CNPJ's com regime tributário do tipo 'Lucro Real'")

st.markdown("Abaixo é mostrado quantos CNPJ's o regime tributário é do tipo 'Lucro real no estado da Paraíba entre os anos de 2014 e 2021'. Os dados estão disponíveis no portal de dados abertos do gverno federal. As informações sobre CNPJs estão [neste Link](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)")


ano = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
cnpj = [241, 243, 274, 298, 318, 358, 400, 441]

fig = px.line(x=ano, y=cnpj, markers=True, title='', text=cnpj)
fig.update_xaxes(title_text='Ano')
fig.update_yaxes(title_text='Quantidade de CNPJ')
fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)
