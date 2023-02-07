import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

# Page config

def form_field(title:str, extra_info:str, space:int, type:str):
    field = html.Div(
        [
            dbc.Label(title, html_for=title.lower() + '_field'),
            dbc.Input(type=type,
                      id=title.lower() + '_field', 
                      placeholder="Enter " + title),
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
            )), class_name='{padding: 10px 50px 20px}')
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