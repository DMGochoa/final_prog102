import dash_bootstrap_components as dbc

from dash import html, dcc, callback, Output, Input

pathname = 'hi'

""" jumbotron = html.Div(
    dbc.Container(
        [
            html.P(
                f"The pathname {pathname} was not recognised...",
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

            dbc.Row(
                        dbc.Col(
                            dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                            width=4
                        ),
                        justify='center'
                    ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",

#) """

jumbotron = html.Div(
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H2('404 - PAGE NOT FOUND',className='card-title'),
                                html.A(dcc.Link('Login',href='/login'))
                            ],
                            body=True
                        )
                    ],
                    width=5
                ),
                justify='center'
            )
        )


