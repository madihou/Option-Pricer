from BSM import BSM
import pickle
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, State, Output, dcc, html, callback


def create_theoretical_layout():

    layout = [html.Div([
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

    return layout


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
    spot_sim = bsm.simulate_spot_price(10)

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
