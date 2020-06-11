# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:39:07 2020

@author: Giovanna Gehring
"""

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



app = dash.Dash(__name__)

server = app.server

#importar dataset
df = pd.read_csv("SAMPLE_ENEM3.csv", delimiter=",", encoding="utf8")


#criar variáveis para usar no dropdown
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
             html.H1("Enem Dashboard"),
    
#nome do dropdown    
    
             html.Label("Variável Socioeconómica"),
                   
#dropdown x_axis
    
             dcc.Dropdown(
             id = "socioeconomico",
             options=x_escolhas,
             value="social"
             ),   
    
#nome do dropdown    
    
             html.Label("Variáveis de Desempenho"),
                   
    
#dropdown y_axis
    
             dcc.Dropdown(
             id = "desempenho",
             options=y_escolhas,
             value="total"
             ),   
    
    
#box plot
             dcc.Graph(id="boxplot"),
        
    
])


#callbacks

@app.callback(Output("boxplot", "figure"),
             [Input("socioeconomico", "value"),
             Input("desempenho", "value")])

def update_figure(selectedx, selectedy): 

#valores da axis x
    if "social" in selectedx:
        x_box = df["GRUPO_SOCIAL"]
    if "escola" in selectedx:
        x_box = df["TIPO_ESCOLA"]
    if "raca" in selectedx:
        x_box = df["TP_COR_RACA"]
    if "edu_pai" in selectedx:
        x_box = df["EDUCACAO_PAI"]
    if "edu_mae" in selectedx:
        x_box = df["EDUCACAO_MAE"]

#valores da axis y
    if "total" in selectedy:
        y_box = df["NU_NOTA_TOTAL"]
    if "natureza" in selectedy:
        y_box = df["NU_NOTA_CN"]
    if "matematica" in selectedy:
        y_box = df["NU_NOTA_MT"]
    if "linguagem" in selectedy:
        y_box = df["NU_NOTA_LC"]
    if "humanas" in selectedy:
        y_box = df["NU_NOTA_CH"]
    if "redacao" in selectedy:
        y_box = df["NU_NOTA_REDACAO"]

    return px.box(df,
            x=y_box,
            y=x_box,
            color=x_box,
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