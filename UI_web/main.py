from dash import Dash, dcc, html, Input, Output, no_update, ALL
import pandas as pd
import plotly.express as px
import json
import dash_bootstrap_components as dbc

# Pages
from pages.register import register_form

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.LUX, 
                                 dbc.icons.BOOTSTRAP], 
           suppress_callback_exceptions=True,
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1"}]
           )

app.title = "Bank"

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    dbc.Row([
        dbc.Col(className="col-2",),
        dbc.Col(register_form(), className="col-8",),
        dbc.Col(className="col-2",),  
        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)