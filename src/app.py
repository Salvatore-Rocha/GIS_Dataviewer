import dash
import plotly.graph_objects as go
from dash import dcc, html, callback
from dash.dependencies import Output, Input, State, MATCH, ALL
import plotly.express as px 
import dash_bootstrap_components as dbc
import pandas as pd
import requests
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio
from dash.exceptions import PreventUpdate
import numpy as np
import joblib
import base64
import io

# Create a Plotly layout with the desired dbc template
load_figure_template(["pulse", "pulse_dark"])
layout = go.Layout(template= pio.templates["pulse"])

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Work Files 
json_file_url = 'https://raw.githubusercontent.com/Salvatore-Rocha/GIS_Dataviewer/4e8c24d98c3b6b9ac5ee4cd08de263316b35a7da/Files/cdmx-alcaldias-4326.json'
response = requests.get(json_file_url)
json_data_alc = response.json()

json_file_url = 'https://raw.githubusercontent.com/Salvatore-Rocha/GIS_Dataviewer/4e8c24d98c3b6b9ac5ee4cd08de263316b35a7da/Files/georef_mex_col_tr.json'
response = requests.get(json_file_url)
json_data_col = response.json()

# CSV File in Githubt (added ?raw=true at the end of the URL or it will not parse it correctly) 
listings = pd.read_csv("https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/4e8c24d98c3b6b9ac5ee4cd08de263316b35a7da/Files/listings_n_col_alc.csv?raw=true")

header = html.H1(
    "Discover Mexico City's Airbnb Scene", 
    className="bg-primary text-white p-2 mb-2 text-center"
                )

sources = html.Div(
    [
        html.P("By Eduardo Salvador Rocha"),
        html.Label(
            [
                "Links: ",
                html.A(
                    "Eduardo's GitHub|  ",
                    href="https://github.com/Salvatore-Rocha/GIS_Dataviewer",
                    target="_blank",
                ),
                html.A(
                    "Code (.py file) |   ",
                    href="https://github.com/Salvatore-Rocha/Supermarket-sales/blob/0344a62c2e0c00b254c93690b5cc873c8cfb77a7/src/app.py",
                    target="_blank",
                
                ),
                html.A(
                    "Code (Jupyter Notebook (Google Colab) |   ",
                    href="https://colab.research.google.com/drive/1Xnx0tj9BDDt_NgxE2d2gdFr93wkmJ-bh?usp=sharing",
                    target="_blank",
                
                ),
            ]
        ),
    ]
)

#The branches are located in Yangon, Naypyitaw, Mandalay
tab1 = dbc.Tab([ 
                dbc.Row([
                    dbc.Col([ # Main text & Prediction params
                            ]
                            ,width= 3),
                    dbc.Col([
                            ])
                        ])
                ], label="Title Tab 1",)
tabs = dbc.Card(dbc.Tabs([tab1], style={'font-style': 'italic'}))


app =  dash.Dash(__name__, 
                 external_stylesheets= [dbc.themes.PULSE, dbc.icons.FONT_AWESOME, dbc_css],)
#server = app.server
app.layout = dbc.Container(style={'padding': '50px'},
    children=[
            header,
            dbc.Row([ #Carrousel with 3 windows
                    tabs
                    ]),
            dbc.Row([ #Links/ Sources
                    sources
                    ]),  
],fluid=True,
  className="dbc dbc-ag-grid")


if __name__=='__main__':
    app.run_server(debug=True, port=8050)
    #app.run_server()