import dash_bootstrap_components as dbc
import dash
import json
from dash import html, dcc, Input, Output, callback, State
from datetime import date

import requests

dash.register_page(__name__, path='/register')

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


def register_form():

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
    dd_type  = dbc.Select(
        id = "dd_type_field",
        options=[
            {"label": "Employee", "value": "Employee"},
            {"label": "User", "value": "User"},
            {"label": "Disabled option", "value": "3", "disabled": True},],
        className="mb-4")

    scheme = html.Div(
        [
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
            )))
        ], className="col-lg-12 col-lg-6 ",
    )
    form = dbc.Form([scheme])
    return form

layout = html.Div(
        dbc.Row(
            [
                dbc.Col(
                    className="col-lg-2",
                ),
                dbc.Col(
                    register_form(),
                    className="col-lg-8",
                ),
                dbc.Col(
                    className="col-lg-2",
                ),
                html.Br(),
                html.Div(id="my-output"),
            ]
        ),
)
# Callback for the register users page
@callback(
    Output(component_id="my-output", component_property="children"),
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
    if n_clicks != 0:
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
        
        user = {
            "first_name": "pedrito",
            "last_name": "mendoza",
            "document_id": "1234545678",
            "type": "client-person",
            "birthday": "1997-01-01",
            "country": "peru",
            "city": "lima",
            "address": "av siempreviva",
            "email": "jm@texample.com",
            "phone_number": "999555999"}
        response = requests.post('http://127.0.0.1:9000/users', json=user)
        print(response)
        print('-'*30)
        print(user_data)
        response = requests.post('http://127.0.0.1:9000/users', json=user_data)
        print('-'*30)
        print(response.headers)
        print('-'*30)
        print(response.json)
        print(response.text)
        
        json_response = json.loads(response.text)
        with open("user_credentials.txt", "w") as f:
            f.write(json.dumps(json_response))
