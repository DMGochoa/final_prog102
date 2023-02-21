import dash_bootstrap_components as dbc
import requests
import dash
import json
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
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

# login layout content
def login_layout():
    return html.Div(
        [
            dcc.Location(id='login-url',pathname='/login',refresh=False),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4('Login',className='card-title'),
                                    dbc.Input(id='login-user',placeholder='User'),
                                    html.Br(),
                                    dbc.Input(id='login-password',placeholder='Assigned password',type='password'),
                                    html.Br(),
                                    dbc.Input(id='login-code',placeholder='Code',type='number'),
                                    html.Br(),
                                    dbc.Button('Submit',id='login-button',color='success'),
                                    html.Br(),
                                    html.Div(id='login-alert'),
                                    html.Div(id="my-output-login"),
                                ],
                                body=True
                            ),
                            width=6
                        ),
                        justify='center'
                    )
                ]
            )
        ]
    )





# authenticate 
@callback(
    [Output('url','pathname'),
     Output('login-alert','children')],
    [Input('login-button','n_clicks')],
    [State('login-user','value'),
     State('login-password','value'),
     State('login-code', 'value')])
def login_auth(n_clicks, user, pw, code):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks==0:
        return no_update, no_update
    credentials = {'username':user,
                   "password":pw,
                   "code" : code}
    if authenticate_user(credentials):
        session['authed'] = True
        logger.debug('############### Token from main.py ##############')
        logger.debug('Searching the info of the User by the token')
        logger.debug(f'The token to search is {token.get_token()}')
        user_info = requests.get('http://127.0.0.1:9000/home', headers={'Authorization':token.get_token()})
        logger.debug(f'The request for the user info is: {user_info.status_code}')
        logger.debug('Saving the info to de info carrier')
        info = json.loads(user_info.text)
        info_carrier.set_general(info['user'][0])
        user_type = info_carrier.get_general()
        logger.debug(f'The info was save and is: {info_carrier.get_general()}')
        if user_type['type'] == 'Employee':
            return '/register', ''
        else:
            return '/home',''
    session['authed'] = False
    return no_update, dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)

