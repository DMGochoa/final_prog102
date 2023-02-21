import dash_bootstrap_components as dbc
import dash
import json
import requests
import base64
import datetime
import pandas as pd
import io
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session

# Utils
from utils.logging_web import log_web
from utils.validation import form_val

# Setup logger
logger = log_web()

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

drag_and_drop = html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files', style={"font-weight": "bold"})
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),
                            html.Div(id='output-data-upload'),
                        ])

# home layout content
@validate_login_session
def file_register_layout():
    logger.debug('Charging the file register layout')
    return \
        html.Div([
            dcc.Location(id='file_register-url',pathname='/file_register'),
            sidebar,
            
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H2('Massive Register'),
                                drag_and_drop,
                            ],
                        ),
                        justify='center',
                        style=CONTENT_STYLE
                    ),

                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                            width=4
                        ),
                        justify='center',
                        style=CONTENT_STYLE
                    ),

                    
                    html.Br(),
                    html.Div([
                                #html.Button("Download CSV", id="btn_csv"),
                                dcc.Download(id="download-dataframe-csv"),
                            ]),
                ],
            )
        ]
    )

@callback(
    Output('file_register-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'

@callback(Output("download-dataframe-csv", "data"),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'),
          prevent_initial_call=True,)
def update_output(contents, filename, last_modified):
    content_type, content_string = contents[0].split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename[0]:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename[0] or 'xlsx' in filename[0]:
            print('entramos')
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df['birthday'] = pd.to_datetime(df.birthday)
            df['birthday'] = df['birthday'].dt.strftime('%Y-%m-%d')
            new_users = df.to_dict('records')
        
        login = {"username": list(), 
                "password": list(), 
                "code": list()}
        
        for user in new_users:
            val, issue = form_val(user)
            if val:
                logger.debug('Send request to save the')
                response = requests.post('http://127.0.0.1:9000/users', json=user)
                logger.debug(f'The response is {response.status_code}')
                
                json_response = json.loads(response.text)
                
                login['username'].append(json_response['username'])
                login['password'].append(json_response['password'])
                login['code'].append(json_response['code'])
                
                #return dbc.Alert('Successfully created',color='success',dismissable=True)
            else:
                logger.debug(f'Mistake occur {val}, the issue is {issue}')
                #return dbc.Alert(issue, color='danger', dismissable=True)
        
        df = pd.DataFrame.from_dict(login)
        
        return dcc.send_data_frame(df.to_csv, "user_info.csv")
    except Exception as e:
        print(e)
