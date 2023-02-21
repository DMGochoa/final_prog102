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
                    html.P("DNI number: "),
                    dbc.Input(id="user_deposit-DNI",type="number", placeholder="Enter user's DNI number",),
                    html.Br(),
                    html.P("Account number: "),
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
                    html.P("DNI number: "),
                    dbc.Input(id="user_withdraw-DNI",type="number", placeholder="Enter user's DNI number",),
                    html.Br(),
                    html.P("Account number: "),
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
                    html.P("Origin Account CBU: "),
                    dbc.Input(id="origin-account", type="number", placeholder="Enter origin account CBU"),
                    html.Br(),
                    dbc.Input(id="trasnfer-amount", type="number", placeholder="$"),
                    html.P("Enter amount to transfer from account"),
                    html.Br(),
                    html.P("Destiny Account CBU: "),
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

                    html.Div(id="user_service-output"),
                    html.Div(id="user_service-outpu"),
                    html.Div(id="user_service-outp"),
                    html.Br(),
                ],
            )
        ]
    )


# Callback for the Deposit transaction
@callback(
    Output("user_service-output", "children"),
    Input("make-deposit", "n_clicks"),
    State("user_deposit-DNI", "value"),
    State("user_deposit-account", "value"),
    State("deposit-amount", "value"),
)
def make_deposit_click(
    n_clicks,
    value_DNI,
    value_account,
    value_amount
):
    logger.debug('Click in the buttom Make deposit')
    if n_clicks is None or n_clicks==0:
        return no_update
    logger.debug('The info from the deposit transactions is save')
    deposit_data = {
        "transaction_type": 'deposit',
        "cbu_origin": value_DNI,
        "cbu_destiny": value_account,
        "description": 'Some random description',
        "amount": value_amount,
    }
    print(deposit_data)
    logger.debug(f'Info for the deposit: {deposit_data}')
    val, issue = deposit_val(deposit_data)
    if val:
        logger.debug('Send request to save the deposit data')
        response = requests.post('http://127.0.0.1:9000/transaction', json=deposit_data)
        if response.status_code == 400:
             return dbc.Alert("Error with account destiny or amount",
                            color='danger',
                            dismissable=True)
        print('-'*30)
        print(response.headers)
        print('-'*30)
        print(response.json)
        print(response.text)
        return dbc.Alert('Deposit sucessfull!!!',
                            color='success',
                            dismissable=True)

    else:
        logger.debug(f'Mistake occur {val}, the issue is {issue}')
        return dbc.Alert(issue,
                            color='danger',
                            dismissable=True)

# Callback for the Withdraw transaction
@callback(
    Output("user_service-outpu", "children"),
    Input("make-withdraw", "n_clicks"),
    State("user_withdraw-DNI", "value"),
    State("user_withdraw-account", "value"),
    State("withdraw-amount", "value"),
)
def make_withdraw_click(
    n_clicks,
    value_DNI,
    value_account,
    value_amount
):
    logger.debug('Click in the buttom Make withdraw')
    if n_clicks is None or n_clicks==0:
        return no_update
    logger.debug('The info from the withdraw transactions is save')
    withdraw_data = {
        "transaction_type": 'withdraw',
        "cbu_origin": value_DNI,
        "cbu_destiny": value_account,
        "description": 'Some random description',
        "amount": value_amount,
    }
    print(withdraw_data)
    logger.debug(f'Info for the withdraw: {withdraw_data}')
    val, issue = withdraw_val(withdraw_data)
    if val:
        logger.debug('Send request to save the withdraw data')
        response = requests.post('http://127.0.0.1:9000/transaction', json=withdraw_data)
        if response.status_code == 400:
             return dbc.Alert("Error with account destiny or amount",
                            color='danger',
                            dismissable=True)
        print('-'*30)
        print(response.headers)
        print('-'*30)
        print(response.json)
        print(response.text)
        return dbc.Alert('Withdraw sucessfull!!!',
                            color='success',
                            dismissable=True)

    else:
        logger.debug(f'Mistake occur {val}, the issue is {issue}')
        return dbc.Alert(issue,
                            color='danger',
                            dismissable=True)

# Callback for the transaction between accounts
@callback(
    Output("user_service-outp", "children"),
    Input("make-transfer", "n_clicks"),
    State("origin-account", "value"),
    State("trasnfer-amount", "value"),
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
        print('-'*30)
        print(response.headers)
        print('-'*30)
        print(response.json)
        print(response.text)
        return dbc.Alert('Transaction sucessfull!!!',
                            color='success',
                            dismissable=True)

    else:
        logger.debug(f'Mistake occur {val}, the issue is {issue}')
        return dbc.Alert(issue,
                            color='danger',
                            dismissable=True)



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
