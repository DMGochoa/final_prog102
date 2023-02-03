from dash import Dash, dcc, html, Input, Output, no_update, ALL
import pandas as pd
import plotly.express as px
import json
import dash_bootstrap_components as dbc

# Pages
from pages.register import register_form

app = Dash(__name__,
           external_stylesheets=[
               dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True,
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1"}]
           )


df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    #html.Div(children='''
    #    Dash: A web application framework for your data.
    #'''),

    #dcc.Graph(
    #    id='example-graph',
    #    figure=fig
    #),

    register_form()
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)