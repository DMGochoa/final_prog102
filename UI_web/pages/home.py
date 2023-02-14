import dash_bootstrap_components as dbc
import dash
import json
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
""" dash.register_page(__name__, path='/') # / means home page

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of home page'),
    ]
) """

# home layout content
@validate_login_session
def home_layout():
    return \
        html.Div([
            dcc.Location(id='home-url',pathname='/home'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2('Home page.')

                            ],
                        ),
                        justify='center'
                    ),

                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                            width=4
                        ),
                        justify='center'
                    ),

                    
                    html.Br()
                ],
            )
        ]
    )
