import dash_bootstrap_components as dbc
import dash
import json
import plotly.express as px
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

user_pages = [
    {
        "name": "Home Page.",
        "path": "/home"
    },
    {
        "name": "Transactions Page.",
        "path": "/transactions"
    },
    {
        "name": "Reports page.",
        "path": "/reports"
    }
]

sidebar = html.Div(
    [
        html.H2("Pages", className="display-4"),
        html.Hr(),
        html.P(
            "Navigate through the page with this menu.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in user_pages
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
df = px.data.gapminder()
# reports layout content
@validate_login_session
def reports_layout():
    df = px.data.gapminder()
    return \
        html.Div([
            dcc.Location(id='reports-url',pathname='/reports'),
            dbc.Container(
                [
                    sidebar,
                    dbc.Row(
                        dbc.Col(
                            [
                                dcc.Dropdown(options=df.continent.unique(),
                                     id='cont-choice'),
                                dbc.Table.from_dataframe(df, id="table", striped=True, bordered=True, hover=True)
                            ],
                        ),
                        justify='center',
                        style=CONTENT_STYLE
                        ),

                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                            width=4
                        ),
                        justify='center',
                        style=CONTENT_STYLE
                    ),

                    
                    html.Br()
                ],
            )
        ]
    )

@callback(
    Output('reports-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'

@callback(
    Output('table', 'df'),
    Input('cont-choice', 'value')
)
def update_graph(value):
    if value is None:
        table = dbc.Table.from_dataframe(df, id="table", striped=True, bordered=True, hover=True)
    else:
        dff = df[df.continent==value]
        table = dbc.Table.from_dataframe(dff, id="table", striped=True, bordered=True, hover=True)
    return table
