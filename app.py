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


#importar dataset
df = pd.read_csv("SAMPLE_ENEM3.csv", delimiter=",", encoding="utf8")

#replace values
df['EDUCACAO_PAI'] = np.where(df['EDUCACAO_PAI'] == "Nunca estudou ou fundamental incompleto", "Nunca estudou <br> ou fundamental <br> incompleto", df['EDUCACAO_PAI'])
df['EDUCACAO_MAE'] = np.where(df['EDUCACAO_MAE'] == "Nunca estudou ou fundamental incompleto", "Nunca estudou <br> ou fundamental <br> incompleto", df['EDUCACAO_MAE'])

#df para o mapa
mapa = df[["SG_UF_RESIDENCIA", "Unidade federativa", "NU_NOTA_TOTAL", "NU_NOTA_REDACAO", "NU_NOTA_CN","NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CH"]]

df_mapa = mapa.groupby(df["Unidade federativa"]).mean().reset_index()
df_mapa.head()

#caminho do geojson com o mapa dos estados brasileiros
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

#variáveis para usar nos dropdown da variável socioeconómica
x_escolhas = [
    {"label": "Grupo Social", "value": "social"},
    {"label": "Tipo de Escola", "value": "escola"},
    {"label": "Raça", "value": "raca"},
    {"label": "Nível Educação Pai", "value": "edu_pai"},
    {"label": "Nível Educação Mãe", "value": "edu_mae"}
]

#variáveis para usar nos dropdown da variável desempenho
y_escolhas = [
    {"label": "Nota Total", "value": "total"},
    {"label": "Nota Redação", "value": "redacao"},
    {"label": "Nota Linguagens e Códigos", "value": "linguagem"},
    {"label": "Nota Matematica", "value": "matematica"},
    {"label": "Nota Ciências da Natureza", "value": "natureza"},
    {"label": "Nota Ciências Humanas", "value": "humanas"}
]

#determina ordem variaveis boxplot
cat = ("Classe A e B", "Classe C", "Classe D e E",
       "Escola Privada", "Parte em Pública e parte em Privada", "Escola Pública",
       "Branca", "Amarela", "Parda", "Preta", "Indígena", "Não declarado",
       "Pós-graduação", "Ensino Superior", "Ensino Médio", "Ensino Fundamental", "Nunca estudou <br> ou fundamental <br> incompleto", "Não sei")

#iniciar app
app = dash.Dash(__name__)

server = app.server

#app layout
app.layout = html.Div([

#Div 2 (imagem, texto, dropdowns & boxplot)
    html.Div([

#Div 4 (imagem, texto & dropdowns)
        html.Div([

#logo ENEM 2017
            html.Div([(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), width="300"))], style={'textAlign': 'center'}),

#logo texto
            html.Div([
                dcc.Markdown("O Exame Nacional do Ensino Médio (ENEM) é realizado anualmente por milhões alunos Brasileiros com fim a ingressar no Ensino Superior.\n"
                 "O objectivo deste dashboard é explorar as diferenças ao nível do desempenho dos alunos, no ENEM de 2017, através das suas variáveis socioeconómicas."
                     ),
# espaçamento entre objectos
            html.Br(),

#nome do dropdown 2
            html.Label("Variável de Desempenho (Mapa, Boxplot & Heatmap)"),

#dropdown 3
            dcc.Dropdown(
                id = "desempenho",
                options=y_escolhas,
                value="total"
                ),
# espaçamento entre objectos
            html.Br(),

# nome do dropdown 2
            html.Label("Variável Socioeconómica (Boxplot & Heatmap)"),

#dropdown 2
            dcc.Dropdown(
                id="socioeconomico",
                options=x_escolhas,
                value="social"
                ),
            ], style={'textAlign': 'left'}),
        ], className='card1 cards'),

#Div 4 (boxplot)
        html.Div([
            dcc.Graph(id="boxplot"),
        ], className='card2 cards'),
    ],className="row"),

#Div 3 (heatmap & mapa)
    html.Div([
        html.Div([
            dcc.Graph(id="heatmap")
            ], className='card3 cards'),
        html.Div([
            dcc.Graph(id="mapa")
            ], className='card4 cards'),
    ],className="row"),

    html.Div([
        html.H5(
            "Desenvolvido por: Daniela Patrício [M20190400] & Giovanna Gehring [M2018067]",
            style={"margin-top": "0px", "color": "white", 'textAlign': 'center'}
        )
    ])
])

# callback boxplot
@app.callback(Output("boxplot", "figure"),
              [Input("socioeconomico", "value"),
               Input("desempenho", "value")])

def update_figure(selectedx, selectedy):
    # valores da axis x
    if "social" in selectedx:
        x_box = df["GRUPO_SOCIAL"]
        s = "Grupo Social"
    if "escola" in selectedx:
        x_box = df["TIPO_ESCOLA"]
        s = "Tipo de Escola"
    if "raca" in selectedx:
        x_box = df["TP_COR_RACA"]
        s = "Raça"
    if "edu_pai" in selectedx:
        x_box = df["EDUCACAO_PAI"]
        s = "Educação do Pai"
    if "edu_mae" in selectedx:
        x_box = df["EDUCACAO_MAE"]
        s = "Educação da Mãe"

    # valores da axis y
    if "total" in selectedy:
        y_box = df["NU_NOTA_TOTAL"]
        n = "Nota Total"
    if "natureza" in selectedy:
        y_box = df["NU_NOTA_CN"]
        n = "Nota Ciências da Natureza"
    if "matematica" in selectedy:
        y_box = df["NU_NOTA_MT"]
        n = "Nota Matemática"
    if "linguagem" in selectedy:
        y_box = df["NU_NOTA_LC"]
        n = "Nota Linguagens e Códigos"
    if "humanas" in selectedy:
        y_box = df["NU_NOTA_CH"]
        n = "Nota Ciências Humanas"
    if "redacao" in selectedy:
        y_box = df["NU_NOTA_REDACAO"]
        n = "Nota Redação"

    boxplot = go.Box(x=x_box,
                     y=y_box,
                     # orientation="h",
                     marker=dict(color="rgb(31,158,137)", opacity=0.2))

    layout_box = go.Layout(title=s + " vs " + n,
                           title_x=0.5,
                           xaxis=dict(categoryorder="array", categoryarray=cat),
                           yaxis=dict(zeroline=False,
                                      gridcolor='rgb(242, 242, 242)'),
                           plot_bgcolor='rgb(255, 255, 255)',
                           margin=dict(
                               l=40,
                               r=30,
                               b=80,
                               t=100
                           ))

    fig = go.Figure(data=boxplot, layout=layout_box)

    return fig

# callback heatmap
@app.callback(Output("heatmap", "figure"),
              [Input("socioeconomico", "value"),
               Input("desempenho", "value")])

def update_figure(selectedx1, selectedy1):
    # valores da axis x
    if "social" in selectedx1:
        x_heat = df["GRUPO_SOCIAL"]
        s = "Grupo Social"
    if "escola" in selectedx1:
        x_heat = df["TIPO_ESCOLA"]
        s = "Tipo de Escola"
    if "raca" in selectedx1:
        x_heat = df["TP_COR_RACA"]
        s = "Raça"
    if "edu_pai" in selectedx1:
        x_heat = df["EDUCACAO_PAI"]
        s = "Educação do Pai"
    if "edu_mae" in selectedx1:
        x_heat = df["EDUCACAO_MAE"]
        s = "Educação do Mãe"

    # valores da axis y
    if "total" in selectedy1:
        z_heat = df["NU_NOTA_TOTAL"]
        disciplina = "Total"
    if "natureza" in selectedy1:
        z_heat = df["NU_NOTA_CN"]
        disciplina = "Ciências da Natureza"
    if "matematica" in selectedy1:
        z_heat = df["NU_NOTA_MT"]
        disciplina = "Matemática"
    if "linguagem" in selectedy1:
        z_heat = df["NU_NOTA_LC"]
        disciplina = "Linguagens e Códigos"
    if "humanas" in selectedy1:
        z_heat = df["NU_NOTA_CH"]
        disciplina = "Ciências Humanas"
    if "redacao" in selectedy1:
        z_heat = df["NU_NOTA_REDACAO"]
        disciplina = "Redação"

    heatmap = px.density_heatmap(df, x=x_heat,
                                 y=df["Regiao"],
                                 z=z_heat,
                                 histfunc="avg",
                                 color_continuous_scale="Viridis",
                                 category_orders={"GRUPO_SOCIAL": ["Classe A e B", "Classe C", "Classe D e E"],
                                                  "TIPO_ESCOLA": ["Escola Privada",
                                                                  "Parte em Pública e parte em Privada",
                                                                  "Escola Pública"],
                                                  "TP_COR_RACA": ["Branca", "Amarela", "Parda", "Preta", "Indígena",
                                                                  "Não declarado"],
                                                  "EDUCACAO_PAI": ["Pós-graduação", "Ensino Superior", "Ensino Médio",
                                                                   "Ensino Fundamental",
                                                                   "Nunca estudou <br> ou fundamental <br> incompleto",
                                                                   "Não sei"],
                                                  "EDUCACAO_MAE": ["Pós-graduação", "Ensino Superior", "Ensino Médio",
                                                                   "Ensino Fundamental",
                                                                   "Nunca estudou <br> ou fundamental <br> incompleto",
                                                                   "Não sei"]},
                                 labels={"GRUPO_SOCIAL": "Classe Social",
                                         "TIPO_ESCOLA": "Tipo de Escola",
                                         "TP_COR_RACA": "Raça",
                                         "EDUCACAO_PAI": "Nível Educação Pai",
                                         "EDUCACAO_MAE": "Nível Educação Mãe",
                                         "NU_NOTA_TOTAL": "Nota Final",
                                         "NU_NOTA_CN": "Nota Ciências da Natureza",
                                         "NU_NOTA_CH": "Nota Ciências Humanas",
                                         "NU_NOTA_REDACAO": "Nota Redação",
                                         "NU_NOTA_LC": "Nota Linguagens e Códigos",
                                         "NU_NOTA_MT": "Nota Matemática"
                                        }
                                 )


    title2 = "Nota Média " + "<br>" + disciplina
    title3 = "Região vs " + s

    fig2 = go.Figure(data=heatmap)

    fig2.update_layout(coloraxis_colorbar=dict(
        title=title2))
    fig2.update_layout(title_text=title3, title_x=0.5)
    fig2.update_xaxes(title_text="", side="top")
    fig2.update_yaxes(title_text="")

    return fig2

#callback mapa
@app.callback(Output("mapa", "figure"),
             [Input("desempenho", "value")])

def update_figure(selectedy):

    if "total" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_TOTAL"],2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_TOTAL"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_TOTAL"]),2)
        disciplina = "Total"

    if "natureza" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_CN"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_CN"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_CN"]),2)
        disciplina = "Ciências da Natureza"

    if "matematica" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_MT"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_MT"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_MT"]),2)
        disciplina = "Matemática"

    if "linguagem" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_LC"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_LC"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_LC"]),2)
        disciplina = "Linguagens e Códigos"

    if "humanas" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_CH"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_CH"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_CH"]),2)
        disciplina = "Ciências Humanas"

    if "redacao" in selectedy:
        y_1 = round(df_mapa["NU_NOTA_REDACAO"], 2)
        x = df_mapa["Unidade federativa"]
        minmed = round(min(df_mapa["NU_NOTA_REDACAO"]),2)
        maxmed = round(max(df_mapa["NU_NOTA_REDACAO"]),2)
        disciplina = "Redação"

    title2 = "Nota Média " + "<br>" + disciplina

#configuração e apresentação do mapa
    mapa = px.choropleth_mapbox(df_mapa, geojson=data_geo, locations=x, color=y_1,
                         color_continuous_scale="Viridis",
                         range_color=(minmed, maxmed),
                         mapbox_style="carto-positron",
                         center={"lat": -15.4357, "lon": -53.8510},
                         zoom=2,
                         opacity=0.75,
                         labels={"locations": "Estado", "color": title2}
                         )

    title3 = "Nota Média " + disciplina + " por Estado"

    fig3 = go.Figure(data=mapa)
    fig3.update_layout(title_text=title3, title_x=0.5)

    return fig3

#run the application
if __name__ == '__main__':
    app.run_server()