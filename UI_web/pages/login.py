import dash_bootstrap_components as dbc
import requests
import dash
import json
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session


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
        return '/home',''
    session['authed'] = False
    return no_update, dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)



""" # Callback for the register users page
@callback(
    Output("my-output-login", "children"),
    Input("login-button", "n_clicks"),
    State("login-user", "value"),
    State("login-password", "value"),
)
def on_button_click(
    n_clicks,
    value_username,
    value_password,
):
    if n_clicks is None or n_clicks==0:
        return no_update
    user_data = {
        "username": value_username,
        "password": value_password,
            }
 """