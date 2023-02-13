import pandas as pd
import dash
import json
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, no_update, ALL, State
from flask import session, copy_current_request_context
from auth import authenticate_user, validate_login_session
from pages.login import login_layout
from pages.home import home_layout
from pages.register import register_layout
from pages.file_register import file_register_layout
from pages.transactions import transactions_layout
from pages.reports import reports_layout
from components.jumbotron import jumbotron


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

# router
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
)
def router(url):
    if url=='/home':
        return home_layout()
    elif url=='/login' or url=='/':
        return login_layout()
    elif url=='/register':
        return register_layout()
    elif url=='/file_register':
        return file_register_layout()
    elif url=='/reports':
        return reports_layout()
    elif url=='/transactions':
        return transactions_layout()
    else:
        return jumbotron

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
