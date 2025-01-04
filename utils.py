import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# engine para consultas no banco de dados
conn = create_engine('mssql+pyodbc://@localhost/ContosoRetailDW?driver=ODBC+Driver+17+for+SQL+Server')

# função para gráfico de linhas
def lineplot(data, x_axis, y_axis):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.set_theme(style="whitegrid")

    ax.set_title(f'{y_axis} evolution by {x_axis}', fontdict={'fontsize': 18, 'fontweight': 'bold'})

    ax = sns.lineplot(
                    data=data.groupby(x_axis)[y_axis].sum().reset_index(),
                    x=x_axis,
                    y=y_axis,
                    ax=ax)
    
    ax.set_xlabel('')
    #ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
    ax.xaxis.set_tick_params(rotation=45)

    fig.tight_layout()

    return fig

# função para gráfico de barras
def barplot(data, x_axis, y_axis):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.set_theme(style="whitegrid")

    ax.set_title(f'{y_axis} by {x_axis}', fontdict={'fontsize': 18, 'fontweight': 'bold'})

    ax = sns.barplot(
                    data=data.groupby(x_axis)[y_axis].sum().reset_index().sort_values(y_axis, ascending=False).head(15),
                    x=x_axis,
                    y=y_axis,
                    ax=ax)
    
    ax.set_xlabel('')
    #ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
    ax.xaxis.set_tick_params(rotation=45)

    fig.tight_layout()

    return fig

# função para gráfico de calor
def heatmapplot(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.set_theme(style='whitegrid')

    ax.set_title('Correlation Matrix', fontdict={'fontsize': 18, 'fontweight': 'bold'})

    ax = sns.heatmap(
                data,
                annot=True,
                fmt='.2f',
                cmap='coolwarm',
                square=True,
                linewidths=0.5
            )

    fig.tight_layout()

    return fig