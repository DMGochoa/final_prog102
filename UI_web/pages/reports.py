import dash_bootstrap_components as dbc
import dash
import json
import pandas as pd
import requests
import datetime

import plotly.express as px
from dash import html, dcc, Input, Output, callback, State, no_update, dash_table
from auth import authenticate_user, validate_login_session
from flask import session

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
df = px.data.gapminder()

def table(df, continent=None):
    dff = df[df.continent==continent]
    return dff

def years_data(years=[]):
    return [{'label': str(year), 'value': year} for year in years]

# reports layout content
@validate_login_session
def reports_layout():
    df = px.data.gapminder()
    accounts = [account['cbu'] for account in info_carrier.get_specific()]
    months = [{'label': str(i), 'value': i} for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
    col_name = [{"name": i, "id": i} for i in ['amount', 'date', 'description', 'final_account', 'origin_account', 'type']]
    
    return \
        html.Div([
            dcc.Location(id='reports-url',pathname='/reports'),
            dbc.Container(
                [
                    sidebar,
                    dbc.Row(
                        [
                        dbc.Col(
                            [
                                dcc.Dropdown(options=accounts, id='cont-choice'),
                            ],
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(options=years_data(), id='year-choice'),
                            ],
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(options=months, id='month-choice'),
                            ],
                        ),
                        dash_table.DataTable(id = 'table', columns=col_name),    
                        ],
                    justify='center',
                    style=CONTENT_STYLE),

                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                            width=4
                        ),
                        justify='center',
                        style=CONTENT_STYLE
                    ),

                    
                    html.Br()
                ],
            )
        ]
    )

@callback(
    Output('reports-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'

@callback(
    Output('table', 'data'),
    Output('year-choice', 'options'),
    Input('cont-choice', 'value'),
    Input('year-choice', 'value'),
    Input('month-choice', 'value')
)
def update_graph(value, year, month):
    response = requests.get(f'http://127.0.0.1:9000/account/{value}')
    data = json.loads(response.text)

    date = datetime.date.fromisoformat(data['creation_date'])
    date_list = [date.year]
    for y in range(datetime.date.today().year-date.year):
        date_list.append(date.year + y)

    print(value, year, month)
    
    if value is None and year is None and month is None:
        dff = df
    else:
        reports = {
            "year": year,
            "month": month,
            "cbu": value
        }

        transactions_report = requests.get('http://127.0.0.1:9000/report_transactions', json=reports)
        dict_transaction = json.loads(transactions_report.text)

        dff = df[df.continent==value]
        
    return dict_transaction['transactions'], years_data(date_list)