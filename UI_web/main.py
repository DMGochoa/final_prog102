from dash import Dash, dcc, html, Input, Output, no_update, ALL, State
import pandas as pd
import plotly.express as px
import json
import dash_bootstrap_components as dbc

# Pages
from pages.register import register_form
from pages.login import login_page
import pages.register as register

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width"}
    ],  # initial-scale=1"}],
)

app.title = "Bank"

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        dbc.Row(
            [
                dbc.Col(
                    className="col-lg-2",
                ),
                dbc.Col(
                    #login_page(),
                    register_form(),
                    className="col-lg-8",
                ),
                dbc.Col(
                    className="col-lg-2",
                ),
                html.Br(),
                html.Div(id="my-output"),
            ]
        ),
    ]
)



if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
