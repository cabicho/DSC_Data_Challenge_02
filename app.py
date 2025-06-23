import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# Carregar os dados
df = pd.read_csv('data/df_P1_Dados_demográficos.csv', encoding='utf-8')

# Filtrar profissionais com conhecimento em Python e SQL
# Assumindo que a área de formação em TI indica conhecimento nessas tecnologias
areas_ti = [
    'Computação / Engenharia de Software / Sistemas de Informação/ TI',
    'Estatística/ Matemática / Matemática Computacional/ Ciências Atuariais'
]

df_ti = df[df['P1_m_Área_de_Formação'].isin(areas_ti)]

# Contar profissionais por estado
prof_por_estado = df_ti['P1_i_1_uf_onde_mora'].value_counts().reset_index()
prof_por_estado.columns = ['UF', 'Quantidade']

# Carregar geodados do Brasil
brasil = gpd.read_file('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson')
brasil.rename(columns={'sigla': 'UF'}, inplace=True)

# Juntar com nossos dados
brasil_data = brasil.merge(prof_por_estado, on='UF', how='left')

# Criar o mapa
fig = px.choropleth(
    brasil_data,
    geojson=brasil_data.geometry,
    locations=brasil_data.index,
    color='Quantidade',
    hover_name='name',
    hover_data=['UF', 'Quantidade'],
    color_continuous_scale='Viridis',
    scope='south america',
    labels={'Quantidade': 'Profissionais de TI'}
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title_text='Profissionais com conhecimento em Python e SQL por estado',
    margin={"r":0,"t":40,"l":0,"b":0}
)

# Criar aplicação Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Distribuição de Profissionais de TI no Brasil"), className="mb-4 text-center")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='mapa', figure=fig), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div([
            html.H4("Resumo:"),
            html.P("Este mapa mostra a concentração de profissionais com formação em áreas relacionadas a Python e SQL (TI, Engenharia de Software, Ciência da Computação) por estado brasileiro."),
            html.P("Os estados mais escuros indicam maior concentração desses profissionais.")
        ]), className="mt-4")
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)