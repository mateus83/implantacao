# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 21:13:55 2023

@author: Mateus Lucas
"""

import pandas as pd
import plotly.express as px
#import matplotlib as mpl
#import matplotlib.pyplot as plt
import streamlit as st

# Carregando a planilha
planilha = pd.read_excel('Controle Implantação ES Nova planilha.xlsx', sheet_name='BANCO DE DADOS')

colunas = {
    'AS-built': 'AS-built validado',
    'Certificação': 'Certificação validada',
    'Plano de fusão': 'Plano de fusão validado',
    'Plano de Ocupação': 'Plano de Ocupação Validado',
    'Relatorio fotografico L': 'Relatorio fotografico L validado',
    'Relatorio fotografico F': 'Relatorio fotografico F validado',
    'Licenciamento': 'Licenciado',
    'Vistoria Fiscal': 'Fiscalizado',
    'Pendência': 'Encontrado pendência?'
}

opcoes_personalizadas = list(colunas.keys())

opcao_selecionada_personalizada = st.sidebar.selectbox('Selecione a documentação', opcoes_personalizadas)

if opcao_selecionada_personalizada != 'Selecione uma opção':
    coluna_selecionada = colunas[opcao_selecionada_personalizada]
else:
    coluna_selecionada = None

# Aplicando filtro na coluna "Sites entregue" por "ENTREGUE"
planilha_filtrada = planilha[planilha['Sites entregue'] == 'ENTREGUE']

# Convertendo a coluna "DATA ENTREGA" para o tipo datetime
planilha_filtrada['DATA ENTREGA'] = pd.to_datetime(planilha_filtrada['DATA ENTREGA'])

# Adicionando uma nova coluna com o mês e o ano no formato de string
planilha_filtrada['MES_ANO'] = planilha_filtrada['DATA ENTREGA'].dt.strftime('%m/%Y')


if coluna_selecionada == 'Licenciado':
    contagem_valores = planilha_filtrada['Licenciado'].value_counts()
    titulo = ''
        
elif coluna_selecionada == 'Fiscalizado':
    contagem_valores = planilha_filtrada['Fiscalizado'].value_counts()
    titulo = 'Vistoria'

elif coluna_selecionada == 'Encontrado pendência?':
    contagem_valores = planilha_filtrada['Encontrado pendência?'].value_counts()
    titulo = 'Pendências'
    
else:
    contagem_valores = planilha_filtrada[coluna_selecionada].value_counts()
    titulo = 'Validado x Reprovado'


# Agrupando os dados por mês e contando a quantidade de vezes que a coluna selecionada contém a palavra "VALIDADO" e "REPROVADO"
agrupado = planilha_filtrada.groupby('MES_ANO')

# Adicionando a opção "todos" na lista de chaves
opcoes = list(agrupado.groups.keys())
opcoes.insert(0, "Todos")

# Criando a selectbox para selecionar o mês/ano
mes_ano_selecionado = st.sidebar.selectbox('Selecione o mês/ano', opcoes)

# Verificando se a opção selecionada é "todos"
if mes_ano_selecionado == "Todos":
    grupo_selecionado = planilha_filtrada
else:
    # Obtendo os dados filtrados para o mês/ano selecionado
    grupo_selecionado = agrupado.get_group(mes_ano_selecionado)
    
dados_agrupados = grupo_selecionado[coluna_selecionada].value_counts()

#mpl.rcParams['figure.figsize'] = [6, 4] # Define o tamanho da figura
#mpl.rcParams['font.size'] = 10 # Define o tamanho da fonte

# Criando o gráfico de pizza
#plt.figure(figsize=(8, 6))
#fig, ax = plt.subplots()
#ax.pie(dados_agrupados, labels=dados_agrupados.index, autopct='%1.1f%%')

# Contando a quantidade de vezes que a palavra "ENTREGUE" aparece na coluna "Sites entregue"
count_entregue = len(grupo_selecionado[grupo_selecionado['Sites entregue'] == 'ENTREGUE'])

# Adicionando o subtítulo ao título do gráfico
#dados_agrupados_str = [f"{item[0]}: {item[1]}" for item in dados_agrupados.items()]
#ax.set_title(f"Contagem de {coluna_selecionada.rsplit(' ', 1)[0]} {titulo} - {mes_ano_selecionado}\n{count_entregue} Sites entregue - {' - '.join(dados_agrupados_str)}", fontsize=12)

# Exibindo o gráfico
#plt.tight_layout()
#st.pyplot(fig)

# Criando o gráfico de pizza
fig = px.pie(dados_agrupados, values=dados_agrupados.values, names=dados_agrupados.index, hole=0.5)

# Adicionando o subtítulo ao título do gráfico
dados_agrupados_str = [f"{item[0]}: {item[1]}" for item in dados_agrupados.items()]
fig.update_layout(title_text=f"Contagem de {coluna_selecionada.rsplit(' ', 1)[0]} {titulo} - {mes_ano_selecionado}\n{count_entregue} Sites entregue - {' - '.join(dados_agrupados_str)}", title_font_size=12)

titulo = f"Contagem de {coluna_selecionada.rsplit(' ', 1)[0]} {titulo} - {mes_ano_selecionado}"\n"{count_entregue} Sites entregue - {' - '.join(dados_agrupados_str)}"

st.write(titulo)

# Exibindo o gráfico
st.plotly_chart(fig)
