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

# user_service layout content
@validate_login_session
def user_service_layout():
    user_info = info_carrier.get_general()
    accounts = info_carrier.get_specific()
    option_accounts = [{"label": f"account {i+1}", "value": f"Account No {accounts[i]['cbu']}"} for i in range(len(accounts))] 

    return \
        html.Div([
            dcc.Location(id='user_service-url',pathname='/user_service'),
            sidebar,
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2('User services for employees')
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
                    dbc.Input(id="user_deposit-account",type="number", placeholder="Enter Account number",),
                    html.Br(),
                    dbc.Input(id="deposit-amount",type="number", placeholder="$"),
                    html.P("Enter amount to deposit"),
                    html.Br(),
                    dbc.Button("Make deposit", id="make-deposit", n_clicks=0)
                ],
                title="Deposit Amount to user Account: ",
            ),
            dbc.AccordionItem(
                [
                    dbc.Input(id="user_withdraw-account", type="number", placeholder="Enter Account Number"),
                    html.Br(),
                    dbc.Input(id="withdraw-amount", type="number", placeholder="$"),
                    html.P("Enter amount to withdraw"),
                    html.Br(),
                    dbc.Button("Make withdraw", id="make-withdraw", n_clicks=0)
                ],
                title="Withdraw from user Account",
            ),
            dbc.AccordionItem(
                [
                    dbc.Input(id="origin-account", type="number", placeholder="Enter origin account CBU"),
                    html.Br(),
                    dbc.Input(id="trasnfer-amount", type="number", placeholder="$"),
                    html.P("Enter amount to transfer from account"),
                    html.Br(),
                    dbc.Input(id="destiny-account", type="number", placeholder="Type destiny account CBU"),
                    html.Br(),
                    dbc.Button("Make transfer", id="make-transfer", n_clicks=0)
                ],
                title="Transfer money between accounts of the same bank",
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
    Output('user_service-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
