import dash_bootstrap_components as dbc
from dash import html

pathname = 'hi'

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.P(
                "The pathname {pathname} was not recognised...",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Use utility classes for typography and spacing to suit the "
                "larger container."
            ),
            html.P(
                dbc.Button("Learn more", color="primary"), className="lead"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)
