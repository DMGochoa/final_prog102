import dash_bootstrap_components as dbc
from dash import html

def form_field(title:str, extra_info:str, space:int):

    field = html.Div(
        [
            dbc.Label(title, html_for=title.lower() + '_field'),
            dbc.Input(type=title.lower(), id=title.lower() + '_field', placeholder="Enter " + title),
            dbc.FormText(
                    extra_info,
                    color="secondary",
                ),
        ],
        className=f"mb-{space}",
    )
    return field

titles = ['Firstname', 'Lastname', 'National ID']
extra_data = ['Please enter the firstname',
              'Please enter the lastname',
              'Please enter your national ID',
            ]


def register_form():
    f_name = form_field('Firstame', 'Please enter the firstname',6)
    l_name = form_field('Lastname', 'Please enter the lastname',3)
    scheme = html.Div(
        [
            dbc.Row([dbc.Col(f_name), 
                    dbc.Col(l_name)])
        ], className="col-12 col-lg-6"
    )

    

    form = dbc.Form([scheme])
    return form