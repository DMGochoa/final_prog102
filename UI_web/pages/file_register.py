import dash_bootstrap_components as dbc
import dash
import json
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session

# Utils
from utils.logging_web import log_web

# Setup logger
logger = log_web()

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

employee_pages = [
    {
        "name": "Register page.",
        "path": "/register"
    },
    {
        "name": "File registration page.",
        "path": "/file_register"
    },
    {
        "name": "User services page.",
        "path": "/user_service"
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
                for page in employee_pages
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# home layout content
@validate_login_session
def file_register_layout():
    logger.debug('Charging the file register layout')
    return \
        html.Div([
            dcc.Location(id='file_register-url',pathname='/file_register'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2('File register page.'),
                                sidebar
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

                    
                    html.Br(),
                ],
            )
        ]
    )

@callback(
    Output('file_register-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
