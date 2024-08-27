import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF

# Função para gerar o PDF
def generate_pdf(cluster_data, cluster_selected):
    pdf = FPDF()
    pdf.add_page()
    
    # Adicionando título
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f'Relatório Detalhado do Cluster {cluster_selected}', ln=True, align='C')
    
    # Estatísticas Descritivas
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, 'Estatísticas Descritivas', ln=True, align='L')
    pdf.set_font('Arial', '', 10)
    for col in cluster_data.columns:
        stats = cluster_data[col].describe()
        pdf.cell(200, 10, f'{col}: {stats}', ln=True)
    
    # Salvando o PDF
    pdf_file = f'analise_cluster_{cluster_selected}.pdf'
    pdf.output(pdf_file)
    return pdf_file

# Carregar os dados
st.title('Relatório de Marketing de Segmentação de Consumidores de Videogames')
data = pd.read_csv('segmented.csv')
st.write('Dados Segmentados', data)

# Distribuição dos clusters
st.subheader('Distribuição dos Clusters')
cluster_counts = data['Cluster'].value_counts()
fig_bar = go.Figure([go.Bar(x=cluster_counts.index, y=cluster_counts.values)])
fig_bar.update_layout(title='Número de Entrevistados por Cluster', xaxis_title='Cluster', yaxis_title='Número de Entrevistados')
st.plotly_chart(fig_bar)

# Análise detalhada por cluster
st.subheader('Análise Detalhada por Cluster')
cluster_selected = st.selectbox('Escolha um Cluster para Analisar:', data['Cluster'].unique())
cluster_data = data[data['Cluster'] == cluster_selected]
st.write(f'Estatísticas Descritivas do Cluster {cluster_selected}', cluster_data.describe())

# Distribuição das variáveis por cluster (dropdown)
st.subheader('Distribuição das Variáveis por Cluster')
variable_selected = st.selectbox('Escolha uma Variável para Analisar:', data.columns[:-1])  # Excluir a coluna do Cluster
fig_hist = px.histogram(cluster_data, x=variable_selected, nbins=20, title=f'Distribuição de {variable_selected} no Cluster {cluster_selected}')
fig_hist.update_layout(bargap=0.1)
st.plotly_chart(fig_hist)

# Gerar PDF com análise completa
if st.button('Baixar Relatório Completo em PDF'):
    pdf_file = generate_pdf(cluster_data, cluster_selected)
    st.success('Relatório gerado com sucesso!')
    st.download_button(label="Clique aqui para baixar o PDF", file_name=pdf_file, mime="application/pdf")

