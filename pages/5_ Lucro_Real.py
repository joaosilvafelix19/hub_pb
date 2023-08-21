import streamlit as st
import plotly.express as px


st.title("Regime tributário do tipo 'Lucro Real'")

st.write("Abaixo é mostrado quantos CNPJ's são do tipo 'Lucro real no estado da Paraíba entre os anos de 2014 e 2021' ")

"""
ano = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
cnpj = [241, 243, 274, 298, 318, 358, 400, 441]

fig = px.line(x=ano, y=cnpj, markers=True, title='', text=cnpj)

fig.update_xaxes(title_text='Ano')
fig.update_yaxes(title_text='Quantidade de CNPJ')

fig.update_traces(textposition="top center")

fig.show()
"""