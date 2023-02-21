import dash_bootstrap_components as dbc
from functools import wraps
from dash import html, dcc
from flask import session
import requests


# Logger
from utils.logging_web import log_web
logger = log_web()
# Token carrier
from utils.token_singleton import Token
token = Token()

# fake users dict
users = {
    'test':'pw'
}

def authenticate_user(credentials):
    '''
    generic authentication function
    returns True if user is correct and False otherwise
    '''
    #
    # BACKEND CONNECTION 
    #cred = {
    #    "username" : "DMoreno",
    #    "password" : "Di4724",
    #    "code" : 52327171
    #}

    logger.debug('Start the POST to the API')
    response = requests.post('http://127.0.0.1:9000/login', 
                             json=credentials)
    if int(response.status_code) == 200:
        authed = True
        token.set_token(response.text)
        logger.debug(f'Response token and save on the singleton: {token.get_token()}')
        logger.debug(f'The status code for the connection is {response.status_code}')
    else:
        authed = False
    logger.debug(f'Authentication value {authed}')

    return authed

def validate_login_session(f):
    '''
    takes a layout function that returns layout objects
    checks if the user is logged in or not through the session. 
    If not, returns an error with link to the login page
    '''
    @wraps(f)
    def wrapper(*args,**kwargs):
        if session.get('authed',None)==True:
            return f(*args,**kwargs)
        return html.Div(
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H2('401 - Unauthorized',className='card-title'),
                                html.A(dcc.Link('Login',href='/login'))
                            ],
                            body=True
                        )
                    ],
                    width=5
                ),
                justify='center'
            )
        )
    return wrapper
