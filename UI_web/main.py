import pandas as pd
import time
import dash
import json
import requests
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, no_update, ALL, State, callback
from flask import session, copy_current_request_context
from auth import authenticate_user, validate_login_session
from pages.login import login_layout
from pages.home import home_layout
from pages.register import register_layout
from pages.file_register import file_register_layout
from pages.transactions import transactions_layout
from pages.reports import reports_layout
from components.jumbotron import jumbotron

# Logger
from utils.logging_web import log_web
logger = log_web()
# Token carrier
from utils.token_singleton import Token
token = Token()
# Info carrier
from utils.data import Data_carrier
info_carrier = Data_carrier()

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width"}
    ],
)

app.config.suppress_callback_exceptions = True
app.title = "Bank"

server = app.server
server.config['SECRET_KEY'] = 'k1LUZ1fZShowB6opoyUIEJkJvS8RBF6MMgmNcDGNmgGYr'

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
	"phone_number": "999555999"
}

# main app layout
app.layout = html.Div(
    [
        dcc.Location(id='url',refresh=False),
        html.Div("Banking App with Dash", 
                 style={
                        'fontSize':50, 
                        'textAlign':'center'
                     }),
        html.Div(
            login_layout(),
            id='page-content'
        ),
    ]
)

# Obtain the token when occur the register
"""@callback(
    Output("my-output-login", "children"),
    Input("login-button", "n_clicks"),
    State("login-user", "value"),
    State("login-password", "value"),
    State('login-code', 'value')
)
def on_button_click(n_clicks, user, pw, code):
    if n_clicks is None or n_clicks==0:
        return no_update
    else:
        time.sleep(1)
        logger.debug('############### Token from main.py ##############')
        logger.debug('Searching the info of the User by the token')
        logger.debug(f'The token to search is {token.get_token()}')
        user_info = requests.get('http://127.0.0.1:9000/home', headers={'Authorization':token.get_token()})
        logger.debug(f'The request for the user info is: {user_info.status_code}')
        logger.debug('Saving the info to de info carrier')
        info = json.loads(user_info.text)
        info_carrier.set_general(info)
        logger.debug(f'The info was save and is: {info_carrier.get_general()}')"""


# router
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
)
def router(url):
    logger.debug('Enter in the router')
    try:
        user_type = info_carrier.get_general()['type']
    except:
        user_type = 'Empty'
    logger.debug(f'The user type is {user_type}')
    
    if url=='/home' and user_type == 'User':
        return home_layout()
    elif url=='/login' or url=='/':
        return login_layout()
    elif url=='/register' and user_type == 'Employee':
        return register_layout()
    elif url=='/file_register' and user_type == 'Employee':
        return file_register_layout()
    elif url=='/reports' and user_type == 'User':
        return reports_layout()
    elif url=='/transactions' and user_type == 'User':
        return transactions_layout()
    else:
        return jumbotron

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
