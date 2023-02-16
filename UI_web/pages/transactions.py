import dash_bootstrap_components as dbc
import dash
import json
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session

# Info carrier
from utils.data import Data_carrier
info_carrier = Data_carrier()

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

# transactions layout content
@validate_login_session
def transactions_layout():
    user_info = info_carrier.get_general()
    accounts = info_carrier.get_specific()
    option_accounts = [{"label": f"account {i+1}", "value": f"Account No {accounts[i]['cbu']}"} for i in range(len(accounts))] 

    return \
        html.Div([
            dcc.Location(id='transactions-url',pathname='/transactions'),
            sidebar,
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2(f'Pick your transaction {user_info["first_name"]} {user_info["last_name"]} : ')
                            ],
                        ),
                        justify='center',
                        style = CONTENT_STYLE
                    ),
                    html.Br(),
                    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Select(
                        placeholder="Select an account",
                        id="select-transfer",
                        options= option_accounts,
                            ),
                    html.Br(),
                    dbc.Input(id="trasnfer-amount", type="number", placeholder="$"),
                    html.P("Enter amount to transfer from account"),
                    html.Br(),
                    dbc.Input(id="destiny-account", type="number", placeholder="Type destiny account cbu"),
                    html.Br(),
                    dbc.Button("Make transfer", id="make-transfer", n_clicks=0)
                ],
                title="Transfer money to other account in the bank",
            ),
        ],
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
    Output('transactions-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
