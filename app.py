import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from unidecode import unidecode

# Carregar os dados
#https://drive.google.com/file/d/1BXzt80duLhge2zryEMxX013QgA4fBKmk/view?usp=sharing
#df = pd.read_csv('https://drive.google.com/file/d/1BXzt80duLhge2zryEMxX013QgA4fBKmk/view?usp=sharing', encoding='utf-8')

df = pd.read_csv('data/df_P1_Dados_demográficos.csv', encoding='utf-8')#, error_bad_lines=False) #encoding='utf-8', error_bad_lines=False
#df = pd.read_csv('https://drive.google.com/file/d/1vtnRcIcXl_k0oQ-MW85Ku6wnm6DNv1u2/view?usp=sharing', encoding='utf-8')

print("Colunas disponíveis no DataFrame:")
print(df.columns.tolist())
# 
# Verificar o nome exato da coluna de formação
# Pode ser necessário ajustar conforme a saída do print acima
coluna_formacao = 'P1_m_Área_de_Formação\''  # Ajuste se necessário
# "P1_m_Área_de_Formação'"
#"P1_m_Área_de_Formação'

# "P1_a_Idade'", "P1_a_1_Faixa_idade'", "P1_b_Genero'", "P1_c_Cor/raca/etnia'", "P1_d_PCD'",
# "P1_e_experiencia_profissional_prejudicada'", 
# "P1_e_1_Não_acredito_que_minha_experiência_profissional_seja_afetada'", 
# "P1_e_2_Experiencia_prejudicada_devido_a_minha_Cor_Raça_Etnia'", "P1_e_3_Experiencia_prejudicada_devido_a_minha_identidade_de_gênero'", 
# "P1_e_4_Experiencia_prejudicada_devido_ao_fato_de_ser_PCD'", "P1_f_aspectos_prejudicados'", 
# "P1_f_1_Quantidade_de_oportunidades_de_emprego/vagas_recebidas'", "P1_f_2_Senioridade_das_vagas_recebidas_em_relação_à_sua_experiência'", 
# "P1_f_3_Aprovação_em_processos_seletivos/entrevistas'", "P1_f_4_Oportunidades_de_progressão_de_carreira'", 
# "P1_f_5_Velocidade_de_progressão_de_carreira'", "P1_f_6_Nível_de_cobrança_no_trabalho/Stress_no_trabalho'", 
# "P1_f_7_Atenção_dada_diante_das_minhas_opiniões_e_ideias'", "P1_f_8_Relação_com_outros_membros_da_empresa,_em_momentos_de_trabalho'", 
# "P1_f_9_Relação_com_outros_membros_da_empresa,_em_momentos_de_integração_e_outros_momentos_fora_do_trabalho'", 
# "P1_g_vive_no_brasil'", "P1_i_Estado_onde_mora'", "P1_i_1_uf_onde_mora'", "P1_i_2_Regiao_onde_mora'", 
# "P1_j_Mudou_de_Estado?'", "P1_k_Regiao_de_origem'", "P1_l_Nivel_de_Ensino'", "P1_m_Área_de_Formação'"

#Ou crie uma coluna baseada em outras informações
df['Area_TI'] = df.apply(lambda x: 'TI' in str(x[coluna_formacao]), axis=1)

# Filtrar profissionais com conhecimento em Python e SQL
# Assumindo que a área de formação em TI indica conhecimento nessas tecnologias
areas_ti = [
    'Computação / Engenharia de Software / Sistemas de Informação/ TI',
    'Estatística/ Matemática / Matemática Computacional/ Ciências Atuariais'
]


#P1_m_Área_de_Formação

#df_ti = df[df['P1_m_Área_de_Formação'].isin(areas_ti)]
if "P1_m_Área_de_Formação'" in df.columns:
    print(df["P1_m_Área_de_Formação'"])
else:
    print("Column not found in CSV!")

df_ti = df[df["P1_m_Área_de_Formação'"].isin(areas_ti)]


# Contar profissionais por estado
prof_por_estado = df_ti["P1_i_1_uf_onde_mora'"].value_counts().reset_index()
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