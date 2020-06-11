#importar pacotes necessários

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np
import urllib.request, json
import base64

#iniciar app
app = dash.Dash(__name__)

server = app.server

#importar dataset
df = pd.read_csv("SAMPLE_ENEM3.csv", delimiter=",", encoding="utf8")

#df para o mapa
mapa = df[["SG_UF_RESIDENCIA", "Unidade federativa", "NU_NOTA_TOTAL", "NU_NOTA_REDACAO", "NU_NOTA_CN","NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_REDACAO"]]

df_mapa = mapa.groupby(df["Unidade federativa"]).mean().reset_index()
df_mapa.head()

#caminho do geojson com o mapa do Brasil
geo_path = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'

#assignar o geojson a uma variável
with urllib.request.urlopen(geo_path) as url:
    data_geo = json.loads(url.read().decode())

#mapear feature id ao nome do estado do mapa geojson
for feature in data_geo['features']:
    feature['id'] = feature['properties']['name']

#configurações da imagem
image_filename = 'enemicon.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#criar variáveis para usar nos dropdowns

x_escolhas = [
    {"label": "Classe Social", "value": "social"},
    {"label": "Tipo de Escola", "value": "escola"},
    {"label": "Raça", "value": "raca"},
    {"label": "Nível Educação Pai", "value": "edu_pai"},
    {"label": "Nível Educação Mãe", "value": "edu_mae"}
]

y_escolhas = [
    {"label": "Nota Total", "value": "total"},
    {"label": "Nota Redação", "value": "redacao"},
    {"label": "Nota Linguagens e Códigos", "value": "linguagem"},
    {"label": "Nota Matematica", "value": "matematica"},
    {"label": "Nota Ciências da Natureza", "value": "natureza"},
    {"label": "Nota Ciências Humanas", "value": "humanas"}
]

#app layout
app.layout = html.Div([

#titulo    

            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),

# espaçamento entre objectos
            dcc.Markdown("O Exame Nacional do Ensino Médio (ENEM) é realizado anualmente por milhões alunos Brasileiros com fim a ingressar no Ensino Superior. "
                 "O objectivo deste dashboard é apresentar as diferenças ao nível do desempenho dos alunos nas suas variáveis socioeconómicas. "
                 ),

# espaçamento entre objectos
            html.Br(),

#nome do dropdown 2
             html.Label("Variável de Desempenho,"),

#dropdown 3
             dcc.Dropdown(
             id = "desempenho",
             options=y_escolhas,
             value="total"
             ),
# espaçamento entre objectos
             html.Br(),

#map
            dcc.Graph(id="map"),

# nome do dropdown 2
            html.Label("Variável Socioeconómica"),

#dropdown 2
            dcc.Dropdown(
            id="socioeconomico",
            options=x_escolhas,
            value="social"
            ),


             dcc.Graph(id="boxplot"),


])

#callback1
@app.callback(Output("map", "figure"),
             [Input("desempenho", "value")])

def update_figure(selectedy):

    if "total" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_TOTAL"],2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_TOTAL"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_TOTAL"]),2)

    if "natureza" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_CN"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_CN"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_CN"]),2)

    if "matematica" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_MT"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_MT"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_MT"]),2)

    if "linguagem" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_LC"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_LC"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_LC"]),2)

    if "humanas" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_CH"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_CH"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_CH"]),2)

    if "redacao" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_REDACAO"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_REDACAO"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_REDACAO"]),2)

#configuração e apresentação do mapa
    return px.choropleth_mapbox(df_mapa, geojson=data_geo, locations=x, color=y_1,
                           color_continuous_scale="Viridis",
                           range_color=(minmed, maxmed),
                           mapbox_style="carto-positron",
                           center={"lat": -15.4357, "lon": -53.8510},
                           zoom=3.75,
                           opacity=0.5,
                           labels={"locations": "Estado", "color": "Nota Média"}
                           )

#callback2
@app.callback(Output("boxplot", "figure"),
             [Input("socioeconomico", "value"),
             Input("desempenho", "value")])

def update_figure(selectedx, selectedy):

#valores da variável de socioeconómica
    if "social" in selectedx:
        x_2 = df["GRUPO_SOCIAL"]
    if "escola" in selectedx:
        x_2 = df["TIPO_ESCOLA"]
    if "raca" in selectedx:
        x_2 = df["TP_COR_RACA"]
    if "edu_pai" in selectedx:
        x_2 = df["EDUCACAO_PAI"]
    if "edu_mae" in selectedx:
        x_2 = df["EDUCACAO_MAE"]

#valores da variável de desempenho
    if "total" in selectedy:
        y_2 = df["NU_NOTA_TOTAL"]
    if "natureza" in selectedy:
        y_2 = df["NU_NOTA_CN"]
    if "matematica" in selectedy:
        y_2= df["NU_NOTA_MT"]
    if "linguagem" in selectedy:
        y_2 = df["NU_NOTA_LC"]
    if "humanas" in selectedy:
        y_2 = df["NU_NOTA_CH"]
    if "redacao" in selectedy:
        y_2 = df["NU_NOTA_REDACAO"]

    return px.box(df,
            x=y_2,
            y=x_2,
            color=x_2,
            points="outliers",
            orientation="h", #se quisermos o normal, tirar essa parte e mudar x e y
            #range_x=[100,1000],
            boxmode="overlay",
            category_orders={"GRUPO_SOCIAL": ["Classe A e B", "Classe C", "Classe D e E"],
                             "TIPO_ESCOLA": ["Escola Privada", "Parte em Pública e parte em Privada", "Escola Pública"],
                             "TP_COR_RACA": ["Branca", "Amarela", "Parda", "Preta", "Indígena", "Não declarado"],
                             "EDUCACAO_PAI": ["Pós-graduação", "Ensino Superior", "Ensino Médio", "Ensino Fundamental", "Nunca estudou ou fundamental incompleto", "Não sei"],
                             "EDUCACAO_MAE": ["Pós-graduação", "Ensino Superior", "Ensino Médio", "Ensino Fundamental", "Nunca estudou ou fundamental incompleto", "Não sei"]},
            labels={"GRUPO_SOCIAL": "Classe Social",  "TIPO_ESCOLA": "Tipo de Escola", "TP_COR_RACA": "Raça", "EDUCACAO_PAI":"Nível Educação Pai", "EDUCACAO_MAE":"Nível Educação Mãe",
                    "NU_NOTA_TOTAL":"Nota Final", "NU_NOTA_CN":"Nota Ciências da Natureza", "NU_NOTA_CH":"Nota Ciências Humanas", "NU_NOTA_REDACAO":"Nota Redação",
                    "NU_NOTA_LC":"Nota Linguagens e Códigos", "NU_NOTA_MT":"Nota Matemática"
                   })

#run the application
if __name__ == '__main__':
    app.run_server()