from dash import Dash, dcc, html, Input, Output, no_update, ALL, State
import pandas as pd
import dash
import plotly.express as px
import json
import dash_bootstrap_components as dbc

# Pages
#from pages.register import register_form
#from pages.login import login_page


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    use_pages=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width"}
    ],  # initial-scale=1"}],
)

app.title = "Bank"

app.layout = html.Div(
    [
        # main app framework
        html.Div("Banking App with Dash", style={'fontSize':50, 'textAlign':'center'}),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)



if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
