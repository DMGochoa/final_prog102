import dash_bootstrap_components as dbc
import dash
import json
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session

""" dash.register_page(__name__, path='/login')
# component styling
LOGIN_STYLE = {
    #"display": "flex",
    "justify-content": "space-between",
    "width": "80rem",
    #"padding": "2px 1px",
    "background-color": "#f8f9fa",
}
INPUT_STYLE = {
    "border": "2px solid black",
    "border-radius": "4px",
    "width":"20rem"
}

# Page config

def form_field(title:str, extra_info:str, space:int, type:str):
    field = html.Div(
        [
            dbc.Label(title, html_for=title.lower() + '_field'),
            dbc.Input(type=type,
                      id=title.lower() + '_field', 
                      placeholder="Enter " + title,
                      style=INPUT_STYLE),
            dbc.FormText(
                    extra_info,
                   color="secondary",
                ),
        ],
        className=f"mb-{space}",
    )
    return field

def login_elements():
    username = form_field(title='Username', extra_info='', space=12, type='text')
    password = form_field(title='Password', extra_info='', space=12, type='password')
    
    template = html.Div([
        dbc.Col([
            dbc.Row(username),
            dbc.Row(password),
            dbc.Row(html.Center(html.P(
                dbc.Button("Login", id="submit-button-login", color="primary", n_clicks=0),
            )), style={"justify-content": "space-between",
                       "margin": "1rem",})
        ])
    ])
    return template

def login_page():
    output_page = html.Div([
        dbc.Col([
            dbc.Row([
                dbc.Col(html.P('General bank info'), className="col-lg-8"),
                dbc.Col([login_elements()], className="col-lg-4"),
            ])])
    ])
    return output_page

layout = html.Div(
        dbc.Row(
            [
                dbc.Col(
                    className="col-lg-2",
                ),
                dbc.Col(
                    login_page(),
                    className="col-lg-8",
                    style=LOGIN_STYLE
                ),
                dbc.Col(
                    className="col-lg-2",
                ),
                html.Br(),
                html.Div(id="my-output-login"),
            ]
        ),
) """



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
     State('login-password','value')])
def login_auth(n_clicks,user,pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks==0:
        return no_update,no_update
    credentials = {'user':user,"password":pw}
    if authenticate_user(credentials):
        session['authed'] = True
        return '/home',''
    session['authed'] = False
    return no_update,dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)

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

# Callback for the register users page
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
    print(user_data)