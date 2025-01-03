import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils import conn

# parâmetros da pagina
st.set_page_config(
	page_title='Dashboard Contoso',
	page_icon=':bar_chart:',
	layout='wide',
	initial_sidebar_state='auto'
)

# Query para buscar os dados
query = """
    SELECT TOP 1000
	SalesKey
	,YEAR(DateKey) AS SaleYear
	,DATENAME(MONTH, DateKey) AS SaleMonth
	,DAY(DateKey) as SaleDay
	,CAST(DateKey AS DATE) AS SaleDate
	,e.ChannelName
	,c.SalesTerritoryCountry
	,c.SalesTerritoryRegion
	,c.SalesTerritoryName
	,d.CityName
	,b.StoreType
	,b.StoreName
	,h.ProductCategoryName
	,g.ProductSubcategoryName
	,f.ClassName
	,f.BrandName
	,f.ProductName
	,TotalCost
	,SalesQuantity
	,SalesAmount
	,DiscountQuantity
	,DiscountAmount
	,ReturnQuantity
	,ReturnAmount	
FROM
	FactSales a
LEFT JOIN DimStore b
	ON a.StoreKey = b.StoreKey
LEFT JOIN DimSalesTerritory c
	ON b.GeographyKey = c.GeographyKey
LEFT JOIN DimGeography d
	ON b.GeographyKey = d.GeographyKey
LEFT JOIN DimChannel e
	ON a.channelKey = e.ChannelKey
LEFT JOIN DimProduct f
	ON a.ProductKey = f.ProductKey
LEFT JOIN DimProductSubcategory g
	ON f.ProductSubcategoryKey = g.ProductSubcategoryKey
LEFT JOIN DimProductCategory h
	ON g.ProductCategoryKey = h.ProductCategoryKey
    """

# Lendo os dados
dados = pd.read_sql(query, conn)

# tratamento dos dados
dados['SaleYear'] = dados['SaleYear'].astype('str')

# Criando a aplicação
st.title('Dashboard Contoso')

st.write('## Análise de Desempenho')

tab1, tab2, tab3 = st.tabs(['Análise Exploratória', 'Dashboard', 'Tabela detalhada'])

with tab1:

	st.write('## Análise Exploratória')

	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# gráfico com evolução de vendas
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style="whitegrid")

			ax.set_title('Evolução de Vendas', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.lineplot(
							data=dados.groupby('SaleDate').agg({'SalesAmount':'sum'}),
							x='SaleDate',
							y='SalesAmount',
							ax=ax)
			
			ax.set_xlabel('')
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)

		with col2:
			# gráfico com vendas por ano
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style="whitegrid")

			ax.set_title('Vendas por Ano', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.barplot(
							data=dados.groupby('SaleYear')['SalesAmount'].sum().reset_index(),
							x='SaleYear',
							y='SalesAmount',
							ax=ax)
			
			ax.set_xlabel('')
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)

	st.markdown("""
				* O ano com maior montante de vendas em valor foi 2007
				* Tendencia de queda das vendas entre Janeiro e Maio
				* Em 2010 a venda durante o ano cai entre Junho e Dezembro, diferente dos dois anos anteriores que tem um aumento em Dezembro
				""")

	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# gráfico com vendas por país
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style='whitegrid')

			ax.set_title('Vendas por País', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.barplot(
							data=dados.groupby('SalesTerritoryCountry')['SalesAmount'].sum().reset_index().sort_values('SalesAmount', ascending=False).head(15),
							x='SalesTerritoryCountry',
							y='SalesAmount',
							ax=ax)

			ax.set_xlabel('')
			ax.xaxis.set_tick_params(rotation=45)
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)

			

		with col2:
			# gráfico com vendas por canal
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style="whitegrid")

			ax.set_title('Vendas por Canal', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.barplot(
							data=dados.groupby('ChannelName')['SalesAmount'].sum().reset_index(),
							x='ChannelName',
							y='SalesAmount',
							ax=ax)
			
			ax.set_xlabel('')
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)


	st.markdown("""
				* EUA lidera o montante de vendas
				* O canal com maior valor em vendas foi Store
			 	""")
	

	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# gráfico com vendas por loja
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style='whitegrid')

			ax.set_title('Vendas por Loja', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.barplot(
							data=dados.groupby('StoreName')['SalesAmount'].sum().reset_index().sort_values('SalesAmount', ascending=False).head(15),
							x='StoreName',
							y='SalesAmount',
							ax=ax)

			ax.set_xlabel('')
			ax.xaxis.set_tick_params(rotation=45)
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)

		with col2:
			# gráfico com vendas por marca
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style="whitegrid")

			ax.set_title('Vendas por Marca', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.barplot(
							data=dados.groupby('BrandName')['SalesAmount'].sum().reset_index().sort_values('SalesAmount', ascending=False).head(15),
							x='BrandName',
							y='SalesAmount',
							ax=ax)
			
			ax.set_xlabel('')
			ax.xaxis.set_tick_params(rotation=45)
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)


	st.markdown("""
				* Entre as 10 primeiras lojas em vendas estão lojas da Europa, América do Norte e Ásia
				* As marcas com maiores valores em venda foram Contoso, Fabrikam, Adventure Works e Proseware
			 	""")
	
	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# gráfico com vendas por classe
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style='whitegrid')

			ax.set_title('Vendas por Classe', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.barplot(
							data=dados.groupby('ClassName')['SalesAmount'].sum().reset_index().sort_values('SalesAmount', ascending=False),
							x='ClassName',
							y='SalesAmount',
							ax=ax)

			ax.set_xlabel('')
			ax.xaxis.set_tick_params(rotation=45)
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)

		with col2:
			# gráfico com vendas por subcategoria
			fig, ax = plt.subplots(figsize=(12, 6))
			sns.set_theme(style="whitegrid")

			ax.set_title('Vendas por Quantidade Vendida', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			ax = sns.barplot(
							data=dados.groupby('SaleYear')['SalesQuantity'].sum().reset_index(),
							x='SaleYear',
							y='SalesQuantity',
							ax=ax)
			
			ax.set_xlabel('')
			ax.xaxis.set_tick_params(rotation=45)
			ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

			fig.tight_layout()

			st.pyplot(fig)


	st.markdown("""
				* Produtos de classe regular lideram as vendas
				* Apesar de 2007 ter o maior montante em vendas, foi 2009 que ficou na frente em vendas em quantidade, o que pode indicar: baixa nos preços, mudança de posicionamento da empresa ou produto, vender mais produtos com preço de venda melhor ou novas concorrências com mesma qualidade e preço menores
			 	""")
	
	with tab2:
		st.write('Desenvolver dashboard')

	with tab3:
		columns = st.multiselect('Selecione as colunas', sorted(dados.columns))
		
		st.dataframe(dados[columns], hide_index=True)

		st.download_button(
			label='Download CSV',
			data=dados[columns].to_csv(index=False),
			file_name='dados.csv',
			mime='text/csv'
		)
