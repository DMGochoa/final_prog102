import dash_bootstrap_components as dbc
import dash
import json
from dash import html, dcc, Input, Output, callback, State
from datetime import date

dash.register_page(__name__, path='/') # / means home page

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of home page'),
    ]
)