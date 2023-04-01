# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 21:13:55 2023

@author: Mateus Lucas
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Carregando a planilha
planilha = pd.read_excel('Controle Implantação ES Nova planilha.xlsx', sheet_name='BANCO DE DADOS')

colunas = {
    'AS-built': 'AS-built validado',
    'Certificação': 'Certificação validada',
    'Plano de fusão': 'Plano de fusão validado',
    'Plano de Ocupação': 'Plano de Ocupação Validado',
    'Relatorio fotografico L': 'Relatorio fotografico L validado',
    'Relatorio fotografico F': 'Relatorio fotografico F validado'
}

opcoes_personalizadas = list(colunas.keys())

opcao_selecionada_personalizada = st.sidebar.selectbox('Selecione a documentação', opcoes_personalizadas)

if opcao_selecionada_personalizada != 'Selecione uma opção':
    coluna_selecionada = colunas[opcao_selecionada_personalizada]
    # fazer alguma ação com a coluna selecionada
else:
    coluna_selecionada = None


# Aplicando filtro na coluna "Sites entregue" por "ENTREGUE"
planilha_filtrada = planilha[planilha['Sites entregue'] == 'ENTREGUE']

# Convertendo a coluna "DATA ENTREGA" para o tipo datetime
planilha_filtrada['DATA ENTREGA'] = pd.to_datetime(planilha_filtrada['DATA ENTREGA'])

# Adicionando uma nova coluna com o mês e o ano no formato de string
planilha_filtrada['MES_ANO'] = planilha_filtrada['DATA ENTREGA'].dt.strftime('%m/%Y')

# Filtrando apenas as linhas que contêm "VALIDADO" ou "REPROVADO" na coluna selecionada
planilha_filtrada = planilha_filtrada[planilha_filtrada[coluna_selecionada].isin(['VALIDADO', 'REPROVADO', 'PENDENTE'])]

# Agrupando os dados por mês e contando a quantidade de vezes que a coluna selecionada contém a palavra "VALIDADO" e "REPROVADO"
agrupado = planilha_filtrada.groupby('MES_ANO')

# Criando a selectbox para selecionar o mês/ano
mes_ano_selecionado = st.sidebar.selectbox('Selecione o mês/ano', agrupado.groups.keys())

# Obtendo os dados filtrados para o mês/ano selecionado
grupo_selecionado = agrupado.get_group(mes_ano_selecionado)
dados_agrupados = grupo_selecionado[coluna_selecionada].value_counts()

# Criando o gráfico de pizza
fig, ax = plt.subplots()
ax.pie(dados_agrupados, labels=dados_agrupados.index, autopct='%1.1f%%')

# Contando a quantidade de vezes que a palavra "ENTREGUE" aparece na coluna "Sites entregue"
count_entregue = len(grupo_selecionado[grupo_selecionado['Sites entregue'] == 'ENTREGUE'])

# Adicionando o subtítulo ao título do gráfico
dados_agrupados_str = [f"{item[0]}: {item[1]}" for item in dados_agrupados.items()]
ax.set_title(f"Contagem de {coluna_selecionada.rsplit(' ', 1)[0]} Validado x Reprovado - {mes_ano_selecionado}\n{count_entregue} Sites entregue - {' - '.join(dados_agrupados_str)}", fontsize=12)


# Exibindo o gráfico
st.pyplot(fig)



