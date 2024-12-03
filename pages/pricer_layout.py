from BSM import BSM
import pickle
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, State, Output, dcc, html, callback


def create_pricer_layout():

    content_layout = [html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody(id="call_result")
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody(id="put_result")
                ])
            ])
        ]),
        html.Div(id="bsm_graph")
    ])]
    
    sidebar_layout = [
            html.H3("BSM Parameters", className="display-9"),
            html.Hr(),
            html.H6("Spot :"),
            dbc.Input(id="spot_input", type="number"),
            html.Br(),
            html.H6("Strike:"),
            dbc.Input(id="strike_input", type="number"),
            html.Br(),
            html.H6("Maturity:"),
            dbc.Input(id="maturity_input", type="number"),
            html.Br(),
            html.H6("Interest rate:"),
            dbc.Input(id="rate_input", type="number", max=1, min=0, step=.01),
            html.Br(),
            html.H6("Volatility:"),
            dcc.Slider(id="volatility_slider", value=0, min=0, max=100,
                       tooltip={"always_visible": True, "template": "{value}%"}),
            dbc.Button(id="compute_button", children="Compute !"),
            html.Hr(),
            html.H3("Spot-Volatility Heat Map", className="display-9"),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.P("Heat map size :")
                ]),
                dbc.Col([
                    dbc.Input(id="hm_size", type="number", min=5)
                ]),
            ]),
            html.Br(),
            html.H6("Spot price range :"),
            dcc.RangeSlider(0, 20, 1, value=[5, 15], id="spot_range"),
            html.Br(),
            html.H6("Volatility range :"),
            dcc.RangeSlider(0, 20, 1, value=[5, 15], id="volatility_range")

    ]
    
    return content_layout, sidebar_layout


@callback(
    Output("call_result", "children"),
    Output("put_result", "children"),
    Output("bsm_graph", "children"),
    State("spot_input", "value"),
    State("strike_input", "value"),
    State("maturity_input", "value"),
    State("rate_input", "value"),
    State("volatility_slider", "value"),
    Input("compute_button", "n_clicks"),
    prevent_initial_call=True
)
def compute_bsm(s0: float, K: float, T: int, r: float, sigma: float, _: int):
    bsm = BSM(s0, K, T, r, sigma/100)
    c, p = bsm.compute_option_price()

    call_result = [html.P(f"${c:.2f}")]
    put_result = [html.P(f"${p:.2f}")]
    graph_result = [
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph()
                    ])
                )
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph()
                    ])
                ])
            ])
        ])
    ]

    return call_result, put_result, graph_result


def draw_spot_simulation(spot: list[np.array], T: int):
    spot_fig = go.Figure()
    n = len(spot[0])
    t = np.linspace(0, T, n)
    for i in range(len(spot)):
        spot_fig.add_trace(
            go.Scatter(
                x=t,
                y=spot[i],
                name=f"simulation {i + 1}"
            )
        )
    spot_fig.update_layout(template="plotly_white")
    return spot_fig
