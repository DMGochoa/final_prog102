import dash_bootstrap_components as dbc
import dash
import json
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
import requests

from flask import session

# Info carrier
from utils.data import Data_carrier
info_carrier = Data_carrier()

# Logger
from utils.logging_web import log_web
logger = log_web()
# Token carrier
from utils.token_singleton import Token
token = Token()

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
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





# home layout content
@validate_login_session
def home_layout():
    accounts_info = requests.get('http://127.0.0.1:9000/accounts', headers={'Authorization':token.get_token()})
    logger.debug(f'The request for the account info is: {accounts_info.status_code}')
    logger.debug('Saving the info to de info carrier')
    info = json.loads(accounts_info.text)
    info_carrier.set_specific(info['accounts'])
    logger.debug(f'The accounts are {info}')
    logger.debug(f'The info was save and is: {info_carrier.get_specific()}')

    user_info_carrier = info_carrier.get_general()
    accounts = info_carrier.get_specific()
    accordion_items =[dbc.AccordionItem(html.P(f"Bank Account {accounts[i]['cbu']}:  {round(accounts[i]['balance'], 2)}$"),title=f"Account {i+1}") for i in range(len(accounts))]
    return \
        html.Div([
            dcc.Location(id='home-url',pathname='/home'),
            sidebar,

            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [

                                html.H2(f'Welcome {user_info_carrier["first_name"]} {user_info_carrier["last_name"]}, here are your accounts: ')
                            ],
                        ),
                        justify='center',
                        style = CONTENT_STYLE
                    ),
                    html.Br(),
                    dbc.Accordion(
                            accordion_items,
        style= CONTENT_STYLE
    ),

                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                            width=4
                        ),
                        justify='center'
                    ),
                    html.Br(),

                ],
            )
        ]
    )


@callback(
    Output('home-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'

