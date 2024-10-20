# Libs Necessárias

# Libs para Modelagem e Matrizez
import numpy as np
import pandas as pd

# Libs para anaálises gráficas
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Lib para ignorar avisos
import warnings

from pyparsing import alphas

# Desabilitando avisos
warnings.filterwarnings('ignore')

#lendo base de dados
Base_Dados = pd.read_csv("Dados_queimadasf.csv")

#lendo base de dados
#Base_Dados = pd.read_csv(r'C:/Users/Francisco/Documents/faculdade/promacao_facudade/python/bigData/Dados_queimadasf')
print(Base_Dados)
# Verificando
Base_Dados.head()

#verificar valores nulos
#Base_Dados.isnull().sum()
plt.figure(figsize=(14,5))
plt.title("Análize de valores nulos")
sns.heatmap(Base_Dados.isnull(),  cbar=False)
#plt.show()

#estatisticas
print(Base_Dados.describe())
#informações sobre a base de dados
print("informações sobre a base de dados\n")
print(Base_Dados.info())
print("\n\n")

# quantidades de campus unicos
print("quantidade de anos unicos\n")
Base_Dados.nunique()
print("\n\n")



# Fazendo o somatório das 12 colunas por ano
meses = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
analise = Base_Dados.groupby(by=['ANO'])[meses].sum()

# Criando uma nova coluna com o somatório dessas 12 colunas
analise['total_queimadas'] = analise.sum(axis=1)

# Configurando o tamanho da figura e estilo antes de criar o gráfico
plt.figure(figsize=(12, 5))
plt.style.use("ggplot")

# Criando o gráfico
plt.title("Total de incêndios por ano de 2017 - 2022")
sns.lineplot(data=analise, x=analise.index, y="total_queimadas", lw=2, color='#ff5555', alpha=0.85)

# Ajustando rótulos dos eixos
plt.xlabel('Ano')
plt.ylabel('Total de Queimadas')

# Exibindo o gráfico
plt.show()

# ------------ incendios por mes ------------------
# Derretendo (melt) o DataFrame para usar os dados originais
analise02 = pd.melt(Base_Dados, value_vars=meses, var_name='Meses', value_name='Numeros')

# Agrupando os dados por mês e somando os números de incêndios de todos os anos
total_por_mes = analise02.groupby('Meses')['Numeros'].sum().reset_index()

total_por_mes['Meses'] = pd.Categorical(total_por_mes['Meses'], categories=meses, ordered=True)
total_por_mes = total_por_mes.sort_values('Meses')

# Criando o gráfico de barras
plt.figure(figsize=(12,6))
sns.barplot(data=total_por_mes, x='Meses', y='Numeros', palette='coolwarm')

# Ajustando rótulos dos eixos
plt.xlabel("Mês")
plt.ylabel("Número Total de Incêndios")

# Título do gráfico
plt.title("Total de Incêndios por Mês (Somatório dos anos 2017 -2022)")

# Exibindo o gráfico
plt.show()


#---------------stados com maiores numeros e ensendios
# Derretendo (melt) o DataFrame para usar os dados originais, incluindo a coluna TYPE (Estados)
analise03 = pd.melt(Base_Dados, id_vars=['TYPE'], value_vars=meses, var_name='Meses', value_name='Numeros')

# Agrupando os dados por TYPE e Mês e somando os números de incêndios
total_por_mes_type = analise03.groupby(['TYPE', 'Meses'])['Numeros'].sum().reset_index()

# Ordenando os meses na ordem correta usando a lista 'meses' que já existe
total_por_mes_type['Meses'] = pd.Categorical(total_por_mes_type['Meses'], categories=meses, ordered=True)
total_por_mes_type = total_por_mes_type.sort_values(['TYPE', 'Meses'])

# Criando o gráfico de barras empilhadas, um gráfico para cada TYPE (Estado)
plt.figure(figsize=(14,7))

# Usando a paleta de cores 'tab20' para uma maior distinção entre os estados
barplot = sns.barplot(data=total_por_mes_type, x='Meses', y='Numeros', hue='TYPE', palette='tab20')

# Ajustando rótulos dos eixos
plt.xlabel("Mês")
plt.ylabel("Número Total de Incêndios")

# Título do gráfico
plt.title("Total de Incêndios por Mês e por Estado (Somatório dos anos 2017 -2022)")

# Colocando a legenda à direita
plt.legend(bbox_to_anchor=(1, 1.05), loc='upper left', borderaxespad=0.)

# Exibindo o gráfico
plt.show()

#====================== somente os estados
# Derretendo (melt) o DataFrame para usar os dados originais, incluindo a coluna TYPE (Estados)
analise04 = pd.melt(Base_Dados, id_vars=['TYPE'], value_vars=meses, var_name='Meses', value_name='Numeros')
# Agrupando os dados por TYPE (Estado) e somando todos os incêndios de todos os meses
total_por_estado = analise04.groupby('TYPE')['Numeros'].sum().reset_index()
# Ordenando os estados do maior para o menor número de incêndios
total_por_estado = total_por_estado.sort_values(by='Numeros', ascending=False)
# Criando um dicionário para garantir que as mesmas cores sejam usadas nos dois gráficos
palette = sns.color_palette('tab20', len(total_por_estado['TYPE'].unique()))
color_dict = dict(zip(sorted(total_por_estado['TYPE'].unique()), palette))
# Criando o gráfico de barras mostrando o total por estado, ordenado, com as mesmas cores
plt.figure(figsize=(14,7))
# Usando o dicionário de cores personalizado
sns.barplot(data=total_por_estado, x='TYPE', y='Numeros', palette=color_dict)
# Ajustando rótulos dos eixos
plt.xlabel("Estados")
plt.ylabel("Número Total de Incêndios")
# Título do gráfico
plt.title("Total de Incêndios por Estado (Somatório dos anos 2017 -2022)")
# Rotacionando os nomes dos estados para facilitar a leitura
plt.xticks(rotation=90)
# Exibindo o gráfico
plt.show()

#======================== mapa do Brasil com os picos de encendios
analise5 = Base_Dados
# Criando uma nova coluna com o somatório dessas 12 colunas
analise5['Total_Incendios'] = Base_Dados[meses].sum(axis=1)
print(Base_Dados.head())
# Definir o centro do mapa no Brasil
mapa_brasil = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
# Adicionar os pontos de incêndio ao mapa
for _, row in Base_Dados.iterrows(): # o _, row significa para ignorar o index das linhas e fazer o prenecimento do mapa
    # Criando marcadores no mapa
    folium.CircleMarker(
        location=[row['LAT'], row['LONG']],
        radius=row['Total_Incendios'] / 2000,  # Ajuste o divisor para adequar o tamanho dos círculos
        color='red',
        fill=True,
        fill_opacity=0.6,
        popup=f"Estado: {row['TYPE']}<br>Total Incêndios: {row['Total_Incendios']}"
    ).add_to(mapa_brasil)

# Exibindo o mapa
mapa_brasil.save("mapa_queimadas_brasil.html")

