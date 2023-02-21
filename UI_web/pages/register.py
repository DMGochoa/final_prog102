import os
import dash_bootstrap_components as dbc
import dash
import json
import requests
from dash import html, dcc, Input, Output, callback, State, no_update
from datetime import date
from auth import authenticate_user, validate_login_session
from flask import session

# Utils
from utils.logging_web import log_web
from utils.validation import form_val

# Setup logger
logger = log_web()

current_path = os.path.join(os.path.dirname(__file__), '..', '..', 'user_credentials.txt')

CONTENT_STYLE = {
    "margin-left": "10rem",
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

def form_field(title:str, extra_info:str, space:int, type:str):
    logger.debug(f"The field {title} is created")
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

titles = ['Firstname', 
          'Lastname', 
          'National ID',
          'Birth Date',
          'Country',
          'City',
          'Address',
          'Email',
          'Cellphone Number']

extra_data = ['Please enter the ' +  titles[0],
              'Please enter the ' + titles[1],
              'Please enter your ' + titles[2],
              'Please enter your ' + titles[3],
              'Please enter your ' + titles[4] + ' of birth',
              'Please enter your ' + titles[5] + ' of birth',
              'Please enter your ' + titles[6],
              'Please enter your ' + titles[7],
              'Please enter your ' + titles[8]
            ]

def create_modal_body(username, password, code, account):
    modale_body = [
        html.P(f"Username: {username}"),
        html.Br(),
        html.P(f"Pasword: {password}"),
        html.Br(),
        html.P(f"Code: {code}"),
        html.Br(),
        html.P(f"New account: {account}"),
        html.Br(),
        dbc.Alert('Successfully created',
                             color='success',
                             dismissable=True)
    ]
    return modale_body

# register layout content
@validate_login_session
def register_layout():
    logger.debug("Creating the register form")
    # The different fields of the form
    f_name = form_field(titles[0], extra_data[0], 8, 'text')
    l_name = form_field(titles[1], extra_data[1], 4, 'text')
    nationid = form_field(titles[2], extra_data[2], 8, 'number')
    country = form_field(titles[4], extra_data[4], 4, 'text')
    city = form_field(titles[5], extra_data[5], 8, 'text')
    address = form_field(titles[6], extra_data[6], 8, 'text')
    email = form_field(titles[7], extra_data[7], 4, 'email')
    cellpho = form_field(titles[8], extra_data[8], 8, 'number')
    # Field for the Date
    logger.debug("Creating the date selector")
    bdate = dcc.DatePickerSingle(
        id="birth date_field",
        month_format='DD/MM/YYYY',
        placeholder='DD/MM/YYYY',
        display_format='DD/MM/YYYY',
        clearable=True,
        date=date.today(),
        style={"border-top": "2px"}
    )
    # Field for the dropdown selector
    logger.debug("Creating the dropdown selector")
    dd_type  = dbc.Select(
        id = "dd_type_field",
        options=[
            {"label": "Employee", "value": "Employee"},
            {"label": "User", "value": "User"},
            {"label": "Disabled option", "value": "3", "disabled": True},],
        className="mb-4")

    form = dbc.Form([html.Div(
        [
            dcc.Location(id='register-url',pathname='/register'),
            sidebar,
            dbc.Row([html.H3('Please enter the following information to create a new user.')]),
            dbc.Row([
                dbc.Col(f_name), 
                dbc.Col(l_name),
            ]),
            dbc.Row([
                dbc.Col(nationid), 
                dbc.Col([
                    html.P('Birthdate'),
                    bdate
                ]),
            ]),
            dbc.Row([
                dbc.Col(country), 
                dbc.Col(city),
            ]),
            dbc.Row([
                dbc.Col(address), 
                dbc.Col(cellpho),
            ]),
            dbc.Row([
                dbc.Col([email]),
                dbc.Col([
                    html.P('User type'),
                    dd_type
                ]),
            ]),
            dbc.Row(html.Center(html.P(
                dbc.Button("SUBMIT", id="submit-button", color="primary", n_clicks=0), className="create_user"
            ))),
            dbc.Row((html.P([
                dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Here is your login information: "), close_button=True),
                                dbc.ModalBody(id="modal-body-register"),
                                dbc.ModalFooter([
                                    dbc.Button(
                                        "Close",
                                        id="close-modal",
                                        className="ms-auto",
                                        n_clicks=0,
                                    ),
                                ],
                                ),
                            ],
                            id="credentials-modal",
                            centered=True,
                            is_open=False,
                        ),
        ])))
        ], className="col-lg-12 col-lg-6 ",
    )])  
    layout = html.Div(
        dbc.Row(
            [
                dbc.Col(
                    className="col-lg-2",
                ),
                dbc.Col(
                    [dbc.Row(form),
                     dbc.Row(html.Div(id='login-alert'),)],

                    className="col-lg-8",
                ),
                dbc.Col(
                    className="col-lg-2",
                ),
                html.Br(),
                html.Div(id="my-output"),
            ]
        ),

        style=CONTENT_STYLE

    )
    logger.debug("The register form is complete")
    return layout


# Callback for the register users page
@callback(
    Output("modal-body-register", "children"),
    Input("submit-button", "n_clicks"),
    State("firstname_field", "value"),
    State("lastname_field", "value"),
    State("national id_field", "value"),
    State("birth date_field", "date"),
    State("country_field", "value"),
    State("city_field", "value"),
    State("address_field", "value"),
    State("cellphone number_field", "value"),
    State("email_field", "value"),
    State("dd_type_field", "value"),
)
def on_button_click(
    n_clicks,
    value_firstname,
    value_lastname,
    value_national_id,
    value_birth_date,
    value_country,
    value_city,
    value_address_field,
    value_cellphone_number,
    value_email,
    value_type,
):
    logger.debug('Click in the buttom')
    if n_clicks != 0:
        logger.debug('The info from the form is save')

        user_data = {
            "first_name": value_firstname,
            "last_name": value_lastname,
            "document_id": value_national_id,
            "type": value_type,
            "birthday": value_birth_date,
            "country": value_country,
            "city": value_city,
            "address": value_address_field,
            "email": value_email,
            "phone_number": value_cellphone_number,
        }
        logger.debug(f'Info for register: {user_data}')
        val, issue = form_val(user_data)
        if val:
            logger.debug('Send request to save the')
            response = requests.post('http://127.0.0.1:9000/users', json=user_data)
            json_response = json.loads(response.text)
            if response.status_code == 400:
             return dbc.Alert("Error invalid user data",
                            color='danger',
                            dismissable=True)
            logger.debug(f'The response is {response.status_code}')
            modal_body = create_modal_body(json_response["username"], json_response["password"], json_response["code"], json_response["account_cbu"])
            logger.debug(f'The credentials created were:  {json_response}')
            with open(current_path, "w") as f:
                f.write(json.dumps(json_response))
            return modal_body

        else:
            logger.debug(f'Mistake occur {val}, the issue is {issue}')
            return dbc.Alert(issue,
                             color='danger',
                             dismissable=True)




@callback(
    Output("credentials-modal", "is_open"),
    Input("submit-button", "n_clicks"), 
    Input("close-modal", "n_clicks"),
    State("credentials-modal", "is_open"),
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callback(
    Output('register-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    return '/login'
