import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils import conn, lineplot, barplot, heatmapplot

# page parameters
st.set_page_config(
	page_title='Dashboard Contoso',
	page_icon=':bar_chart:',
	layout='wide',
	initial_sidebar_state='auto'
)

# read data
with open('queries/sales_data.sql', 'r') as file:
	query = file.read()
	dados = pd.read_sql(query, conn)

# data preparation
dados['SaleYear'] = dados['SaleYear'].astype('str')

# Apply custom CSS
st.markdown(
	"""
	<style>
	.stHeaderContainer {
		background-color: #122444;
		padding: 10px;
		border-radius: 10px;
		color: white;
		text-align: center;
	}
	</style>
	""",
	unsafe_allow_html=True
)
# aplication
st.markdown(
	"""<div class="stHeaderContainer">
			<h1>Dashboard Contoso</h1>
			<h2>Análise de Desempenho</h2>
		</div>
	""",
	unsafe_allow_html=True
	)

tab1, tab2 = st.tabs(['Análise Exploratória', 'Dashboard'])

with tab1:
	st.write('## Análise Exploratória')

	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# graph with sales evolution
			grafico_evolutivo = lineplot(data=dados, x_axis='SaleDate', y_axis='SalesAmount')
			st.pyplot(grafico_evolutivo)

		with col2:
			# graph with sales by year
			vendas_ano = barplot(data=dados, x_axis='SaleYear', y_axis='SalesAmount')
			st.pyplot(vendas_ano)

	st.markdown("""
				* O ano com maior montante de vendas em valor foi 2007
				* Tendencia de queda das vendas entre Janeiro e Maio
				* Em 2010 a venda durante o ano cai entre Junho e Dezembro, diferente dos dois anos anteriores que tem um aumento em Dezembro
				""")

	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# graph with sales by country
			vendas_pais = barplot(data=dados, x_axis='SalesTerritoryCountry', y_axis='SalesAmount')

			st.pyplot(vendas_pais)

		with col2:
			# graph with sales by channel
			vendas_canal = barplot(data=dados, x_axis='ChannelName', y_axis='SalesAmount')
			st.pyplot(vendas_canal)

	st.markdown("""
				* EUA lidera o montante de vendas
				* O canal com maior valor em vendas foi Store
			 	""")
	
	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# graph with sales by store
			vendas_loja = barplot(data=dados, x_axis='StoreName', y_axis='SalesAmount')
			st.pyplot(vendas_loja)

		with col2:
			# graph sales by brand
			vendas_marca = barplot(data=dados, x_axis='BrandName', y_axis='SalesAmount')
			st.pyplot(vendas_marca)

	st.markdown("""
				* Entre as 10 primeiras lojas em vendas estão lojas da Europa, América do Norte e Ásia
				* As marcas com maiores valores em venda foram Contoso, Fabrikam, Adventure Works e Proseware
			 	""")
	
	with st.container():
		col1, col2 = st.columns(2)

		with col1:
		# graph sales by class
			vendas_classe = barplot(data=dados, x_axis='ClassName', y_axis='SalesAmount')
			st.pyplot(vendas_classe)

		with col2:
			# graph salesquantity by year
			venda_voluma_ano = barplot(data=dados, x_axis='SaleYear', y_axis='SalesQuantity')
			st.pyplot(venda_voluma_ano)

	st.markdown("""
				* Produtos de classe regular lideram as vendas
				* Apesar de 2007 ter o maior montante em vendas, foi 2009 que ficou na frente em vendas em quantidade, o que pode indicar: baixa nos preços, mudança de posicionamento da empresa ou produto, vender mais produtos com preço de venda melhor ou novas concorrências com mesma qualidade e preço menores
			 	""")

	with st.container():
		col1, col2 = st.columns(2)

		with col1:
			# graph heatmap
			correlation_matrix = dados[['TotalCost', 'SalesAmount', 'SalesQuantity', 'DiscountAmount', 'ReturnAmount']].corr()
			mapa_valor = heatmapplot(data=correlation_matrix)
			st.pyplot(mapa_valor)

		with col2:
			st.empty()

	st.markdown("""
			 A única correlação forte esta em custo e valor vendido, o que faz sentido e mostra que a empresa repassa os custos que recebe
			 """)
	
	with st.container():
		col1, col2, col3 = st.columns(3)

		with col1:
			# graph with number of stores by year
			store_year, ax = plt.subplots(figsize=(15, 8))
			sns.set_theme(style='whitegrid')

			ax.set_title('Number of stores by year', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			sns.barplot(data=dados.groupby('SaleYear')['StoreName'].nunique().reset_index(), x='SaleYear', y='StoreName', ax=ax)

			ax.set_xlabel('')
			ax.set_ylabel('')
			ax.set_yticks([])
			#ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.xaxis.set_tick_params(rotation=45)
			for p in ax.patches:
				ax.annotate(format(p.get_height(), '.0f'), 
							(p.get_x() + p.get_width() / 2., p.get_height()), 
							ha = 'center', va = 'center', 
							xytext = (0, 9), 
							textcoords = 'offset points')
				
			store_year.tight_layout()

			st.pyplot(store_year)

		with col2:
			# ticket average by year
			average_ticket_year = dados.groupby('SaleYear').apply(
														lambda x: x['SalesAmount'].sum() / x['SalesKey'].nunique()
														).reset_index().rename(columns={0: 'TicketMedio'})

			fig_average_ticket_year, ax = plt.subplots(figsize=(15, 8))
			sns.set_theme(style='whitegrid')

			ax.set_title('Ticket Médio por Ano', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			sns.barplot(data=average_ticket_year, x='SaleYear', y='TicketMedio', ax=ax)

			ax.set_xlabel('')
			ax.set_ylabel('')
			ax.set_yticks([])
			#ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.xaxis.set_tick_params(rotation=45)
			for p in ax.patches:
				ax.annotate(f'R$ {p.get_height():,.2f}', 
							(p.get_x() + p.get_width() / 2., p.get_height()), 
							ha = 'center', va = 'center', 
							xytext = (0, 9), 
							textcoords = 'offset points')
				
			fig_average_ticket_year.tight_layout()

			st.pyplot(fig_average_ticket_year)

		with col3:
			# average quantity of sales by ticket and year
			qtd_cupom_ano = dados.groupby('SaleYear').apply(
																lambda x: x['SalesQuantity'].sum() / x['SalesKey'].nunique()
																).reset_index().rename(columns={0: 'QuantidadeMediaVenda'})

			fig_qtd_cupom_ano, ax = plt.subplots(figsize=(15, 8))
			sns.set_theme(style='whitegrid')

			ax.set_title('Average Quantity of Sales by Ticket and Year ', fontdict={'fontsize': 18, 'fontweight': 'bold'})

			sns.barplot(data=qtd_cupom_ano, x='SaleYear', y='QuantidadeMediaVenda', ax=ax)

			ax.set_xlabel('')
			ax.set_ylabel('')
			ax.set_yticks([])
			#ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
			ax.xaxis.set_tick_params(rotation=45)
			for p in ax.patches:
				ax.annotate(f'{p.get_height():,.2f}', 
							(p.get_x() + p.get_width() / 2., p.get_height()), 
							ha = 'center', va = 'center', 
							xytext = (0, 9), 
							textcoords = 'offset points')
    
			fig_qtd_cupom_ano.tight_layout()

			st.pyplot(fig_qtd_cupom_ano)

	qtd_vendas_ano = (
            dados.groupby('SaleYear')['SalesKey']
            .count()
            .reset_index()
            .rename(columns={'SaleYear':'Year', 'SalesKey': 'Quantity Sales'})
            )

	st.write('## Quantidade de Vendas por Ano')

	qtd_vendas_ano['Var % LY'] = qtd_vendas_ano['Quantity Sales'].pct_change() * 100
	qtd_vendas_ano.style.format({'Quantity Sales': '{:,.0f}', 'Var % LY': '{:.2f}%'})
	st.dataframe(qtd_vendas_ano.style.format({'Quantity Sales': '{:,.0f}', 'Var % LY': '{:.2f}%'}), hide_index=True)

	st.markdown("""
			 * O número de lojas se manteve constante
			 * O ticket médio se manteve aumentou nos anos
			 * A quantidade média de vendas por cupom aumentou nos anos
			 * O número de vendas faturadas caiu nos anos
			 """)
	
	st.markdown('Podemos concluir que existe um **aumento pequeno do ticket médio**, existe um **aumento considerável de quantidade de produtos vendidos por cupom**, o que indica que os produtos vendidos são mais baratos do que costumava-se vender, olhando para a **evolução de vendas o valor diminui ao longo dos anos** e ao analisar a **quantidade de vendas faturadas nos anos houve uma redução considerável** o que pode ser um indicativo de que a empresa esta vendendo produtos mais baratos/sem procura no mercado ou que a concorrência esta vendendo produtos de mesma qualidade e preço menores fazendo com os clientes busquem esses produtos')

	
	with tab2:
		# create filters
		with st.container():
			col1, col2, col3 = st.columns(3)

			with col1:
				sel_ano = st.selectbox('Selecione o ano: ', sorted(dados['SaleYear'].unique()), index=None, placeholder='Selecione uma opção')
				sel_mes = st.selectbox('Selecione o mês: ', sorted(dados['SaleMonth'].unique()), index=None, placeholder='Selecione uma opção')
				sel_dia = st.selectbox('Selecione o dia :', sorted(dados['SaleDay'].unique()), index=None, placeholder='Selecione uma opção')

			with col2:
				sel_pais = st.selectbox('Selecione o país: ', sorted(dados['SalesTerritoryCountry'].unique()), index=None, placeholder='Selecione uma opção')
				sel_loja = st.selectbox('Selecione a loja: ', sorted(dados['StoreName'].unique()), index=None, placeholder='Selecione uma opção')
				sel_marca = st.selectbox('Selecione a marca: ', sorted(dados['BrandName'].unique()), index=None, placeholder='Selecione uma opção')

			with col3:
				sel_canal = st.selectbox('Selecione o canal: ', sorted(dados['ChannelName'].unique()), index=None, placeholder='Selecione uma opção')
				sel_classe = st.selectbox('Selecione a classe: ', sorted(dados['ClassName'].unique()), index=None, placeholder='Selecione uma opção')
				sel_categoria = st.selectbox('Selecione a categoria: ', sorted(dados['ProductCategoryName'].unique()), index=None, placeholder='Selecione uma opção')

			# Apply filters
			filtered_data = dados.copy()

			if sel_ano:
				filtered_data = filtered_data[filtered_data['SaleYear'] == sel_ano]

			if sel_mes:
				filtered_data = filtered_data[filtered_data['SaleMonth'] == sel_mes]

			if sel_dia:
				filtered_data = filtered_data[filtered_data['SaleDay'] == sel_dia]

			if sel_pais:
				filtered_data = filtered_data[filtered_data['SalesTerritoryCountry'] == sel_pais]

			if sel_loja:
				filtered_data = filtered_data[filtered_data['StoreName'] == sel_loja]

			if sel_marca:
				filtered_data = filtered_data[filtered_data['BrandName'] == sel_marca]

			if sel_canal:
				filtered_data = filtered_data[filtered_data['ChannelName'] == sel_canal]

			if sel_classe:
				filtered_data = filtered_data[filtered_data['ClassName'] == sel_classe]

			if sel_categoria:
				filtered_data = filtered_data[filtered_data['ProductCategoryName'] == sel_categoria]

		with st.container():
			col1, col2 = st.columns(2)

			with col1:
				evolucao_volume_vendas = lineplot(data=filtered_data, x_axis='SaleDate', y_axis='SalesQuantity')
				st.pyplot(evolucao_volume_vendas)

			with col2:
				evolucao_valor_vendas = lineplot(data=filtered_data, x_axis='SaleDate', y_axis='SalesAmount')
				st.pyplot(evolucao_valor_vendas)

		with st.container():
			# Display dataframe
			columns = st.multiselect('Selecionar apenas colunas desejadas: ', sorted(filtered_data.columns), placeholder='Selecione as colunas')
			
			if not columns:
				st.dataframe(filtered_data, hide_index=True)

				st.download_button(
				label='Download CSV',
				data=filtered_data.to_csv(index=False),
				file_name='dados.csv',
				mime='text/csv'
			)

			else:
				st.dataframe(filtered_data[columns], hide_index=True)

				st.download_button(
					label='Download CSV',
					data=filtered_data[columns].to_csv(index=False),
					file_name='dados.csv',
					mime='text/csv'
				)
				
