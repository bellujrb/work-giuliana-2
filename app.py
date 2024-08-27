import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.title('Relatório de Marketing de Segmentação de Consumidores de Videogames')

data = pd.read_csv('segmented_videogame_data.csv')

st.write('Dados Segmentados', data)

st.subheader('Distribuição dos Clusters')

cluster_counts = data['Cluster'].value_counts()
fig_bar = go.Figure([go.Bar(x=cluster_counts.index, y=cluster_counts.values)])
fig_bar.update_layout(title='Número de Entrevistados por Cluster', xaxis_title='Cluster', yaxis_title='Número de Entrevistados')
st.plotly_chart(fig_bar)

st.subheader('Análise Detalhada por Cluster')
cluster_selected = st.selectbox('Escolha um Cluster para Analisar:', data['Cluster'].unique())

cluster_data = data[data['Cluster'] == cluster_selected]
st.write(f'Estatísticas Descritivas do Cluster {cluster_selected}', cluster_data.describe())

st.subheader('Distribuição das Variáveis por Cluster')

for column in data.columns[:-1]:  
    fig_hist = px.histogram(cluster_data, x=column, nbins=20, title=f'Distribuição de {column} no Cluster {cluster_selected}')
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist)
