import dash_bootstrap_components as dbc
import dash
import json
import requests
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session

# Utils
from utils.logging_web import log_web
from utils.validation import deposit_val, withdraw_val, transaction_val

# Setup logger
logger = log_web()

# Info carrier
from utils.data import Data_carrier
info_carrier = Data_carrier()

CONTENT_STYLE = {
    "margin-left": "10rem",
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
    option_accounts = [{"label": f"account #{accounts[i]['cbu']}", "value": f"{accounts[i]['cbu']}"} for i in range(len(accounts))] 

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
                    dbc.Input(id="transfer-amount", type="number", placeholder="$"),
                    html.P("Enter amount to transfer from account"),
                    html.Br(),
                    dbc.Input(id="destiny-account", type="number", placeholder="Type destiny account cbu"),
                    html.Br(),
                    dbc.Button("Make transfer", id="make-transfer", n_clicks=0),
                    dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Please confirm the information: "), close_button=True),
                                dbc.ModalBody(id="modal-body"),
                                dbc.ModalFooter([
                                    dbc.Button(
                                        "Confirm",
                                        id="confirm-transaction",
                                        className="ms-auto",
                                        color='success',
                                        n_clicks=0,
                                    ),
                                    dbc.Button(
                                        "Cancel",
                                        id="cancel-transaction",
                                        className="ms-auto",
                                        color='danger',
                                        n_clicks=0,
                                    ),
                                ],
                                ),
                            ],
                            id="confirm-modal",
                            centered=True,
                            is_open=False,
                        ),
                    ],
                    title="Transfer money to other account in the bank",
                ),
        ],style= CONTENT_STYLE
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
                    html.Div(id="transactions-output"),
                    html.Br(),
                ]
            )


@callback(
    Output("modal-body", "children"),
    Input("make-transfer", "n_clicks"),
    State("select-transfer", "value"),
    State("transfer-amount", "value"),
    State("destiny-account", "value"),
)
def create_modal_body(n, origin_account, transfer_amount, destiny_account):
    modale_body = [
        html.P(f"Origin account: {origin_account}"),
        html.Br(),
        html.P(f"Tranfer amount: {transfer_amount} $"),
        html.Br(),
        html.P(f"Destiny account: {destiny_account}"),
        html.Br(),
    ]
    return modale_body

@callback(
    Output("confirm-modal", "is_open"),
    Input("make-transfer", "n_clicks"), 
    Input("cancel-transaction", "n_clicks"),
    Input("confirm-transaction", "n_clicks"),
    State("confirm-modal", "is_open"),
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open

# Callback for the transaction between accounts
@callback(
    Output("transactions-output", "children"),
    Input("confirm-transaction", "n_clicks"),
    State("select-transfer", "value"),
    State("transfer-amount", "value"),
    State("destiny-account", "value"),
    
)
def make_transaction_click(
    n_clicks,
    value_origin,
    value_amount,
    value_destiny
):
    logger.debug('Click in the buttom Make transaction')
    if n_clicks is None or n_clicks==0:
        return no_update
    logger.debug('The info from the transfer transactions is save')
    transaction_data = {
        "transaction_type": 'transaction',
        "cbu_origin": value_origin,
        "cbu_destiny": value_destiny,
        "description": 'Some random description',
        "amount": value_amount,
    }
    print(transaction_data)
    logger.debug(f'Info for the transaction: {transaction_data}')
    val, issue = transaction_val(transaction_data)
    if val:
        logger.debug('Send request to save the transaction data')
        response = requests.post('http://127.0.0.1:9000/transaction', json=transaction_data)
        if response.status_code == 400:
             return dbc.Alert("Error with account destiny or amount",
                            color='danger',
                            dismissable=True)
        logger.debug(f'The response is {response.status_code}')
        return dbc.Alert('Transaction sucessfull!!!',
                         color='success',
                         dismissable=True)

    else:
        logger.debug(f'Mistake occur {val}, the issue is {issue}')
        return dbc.Alert(issue,
                         color='danger',
                         dismissable=True)

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
