import dash_bootstrap_components as dbc
from functools import wraps
from dash import html, dcc
from flask import session
import requests

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
    
    response = requests.post('http://127.0.0.1:9000/login', 
                             json=credentials)
    print(response.status_code)
    
    if int(response.status_code) == 200:
        authed = True
    else:
        authed = False
    #authed = (credentials['user'] in users) and (credentials['password'] == users[credentials['user']])
    # 
    #
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
