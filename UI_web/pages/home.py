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
    accounts = [
    {
        "user_id": 151616,
        "cbu": 14263423431,
        "balance": 147.26,
        "id": 154862
    },
    {
        "user_id": 15162416,
        "cbu": 14265424431,
        "balance": 14.26,
        "id": 1543432862
    },
    {
        "user_id": 151623416,
        "cbu": 142652344431,
        "balance": 1.26,
        "id": 1548423462
    }
    ]

    user_info_carrier = info_carrier.get_general()
    print(user_info_carrier)
    user_info = {
	"first_name": "pedrito",
	"last_name": "mendoza",
	"document_id": "1234545678",
	"type": "client-person",
	"birthday": "1997-01-01",
	"country": "peru",
	"city": "lima",
	"address": "av siempreviva",
	"email": "jm@texample.com",
	"phone_number": "999555999",
    }
    return \
        html.Div([
            dcc.Location(id='home-url',pathname='/home'),
            sidebar,
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2(f'Welcome {user_info["first_name"]} {user_info["last_name"]}, here are your accounts: ')
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
                    html.P(f"Bank Account {accounts[0]['cbu']}:  {accounts[0]['balance']}$"),
                ],
                title="Account 1",
            ),
            dbc.AccordionItem(
                [
                    html.P(f"Bank Account {accounts[1]['cbu']}:  {accounts[1]['balance']}$"),
                ],
                title="Account 2",
            ),
            dbc.AccordionItem(
                html.P(f"Bank Account {accounts[2]['cbu']}:  {accounts[2]['balance']}$"),
                title="Account 3",
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
    Output('home-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
