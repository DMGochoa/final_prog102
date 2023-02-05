import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from datetime import date

def form_field(title:str, extra_info:str, space:int):

    field = html.Div(
        [
            dbc.Label(title, html_for=title.lower() + '_field'),
            dbc.Input(type=title.lower(), id=title.lower() + '_field', placeholder="Enter " + title),
            #dbc.FormText(
            #        extra_info,
            #       color="secondary",
            #    ),
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

    # Selectors
    f_name = form_field(titles[0], extra_data[0], 6)
    l_name = form_field(titles[1], extra_data[1], 3)
    nationid = form_field(titles[2], extra_data[2], 6)
    #bdate = form_field(titles[3], extra_data[3], 3)
    country = form_field(titles[4], extra_data[4], 6)
    city = form_field(titles[5], extra_data[5], 3)
    address = form_field(titles[6], extra_data[6], 6)
    email = form_field(titles[7], extra_data[7], 3)
    cellpho = form_field(titles[8], extra_data[8], 6)

    bdate = dcc.DatePickerSingle(
        month_format='DD/MM/YYYY',
        placeholder='DD/MM/YYYY',
        display_format='DD/MM/YYYY',
        clearable=True,
        date=date.today(),
        style={"border-top": "2px"}
    )

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
                    html.P('something'),
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
                dbc.Col([email])
            ]),
            dbc.Row(html.Center(html.P(
                dbc.Button("SUBMIT", color="primary"), className="create_user"
            )))
        ], className="col-12 col-lg-6 ",
    )
    form = dbc.Form([scheme])
    return form

