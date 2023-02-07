from dash import Dash, dcc, html, Input, Output, no_update, ALL, State
import pandas as pd
import plotly.express as px
import json
import dash_bootstrap_components as dbc

# Pages
from pages.register import register_form
import pages.register as register

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],# initial-scale=1"}],
)

app.title = "Bank"

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        dbc.Row(
            [
                dbc.Col(
                    className="col-2",
                ),
                dbc.Col(
                    register_form(),
                    className="col-8",
                ),
                dbc.Col(
                    className="col-2",
                ),
                html.Br(),
                html.Div(id="my-output"),
            ]
        ),
    ]
)


@app.callback(
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
            "national_id": value_national_id,
            "birth_date": value_birth_date,
            "country": value_country,
            "city": value_city,
            "address_field": value_address_field,
            "cellphone_number": value_cellphone_number,
            "email": value_email,
            "type": value_type
        }
        print(user_data)


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
