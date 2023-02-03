from dash import Dash, dcc, html, Input, Output, no_update, ALL
import pandas as pd
import plotly.express as px
import json
import dash_bootstrap_components as dbc


app = Dash(__name__,
           external_stylesheets=[
               dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True,
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1"}]
           )

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)