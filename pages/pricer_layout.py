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
                    dbc.Input(id="hm_size", type="number", min=5, value=5)
                ]),
            ]),
            html.Br(),
            html.H6("Spot price range :"),
            dcc.RangeSlider(0, 0, 1, value=[0, 0], id="spot_range"),
            html.Br(),
            html.H6("Volatility range :"),
            dcc.RangeSlider(0, 0, 1, value=[0, 0], id="volatility_range")

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
def run_bsm(s0: int, K: int, T: int, r: float, sigma: float, _: int):
    bsm = BSM()
    bsm.initialize_bsm(s0, K, T, r, sigma/100)
    c, p = bsm.compute_option_price()

    call_result = [html.P(f"${c:.2f}")]
    put_result = [html.P(f"${p:.2f}")]

    spot_range = [s0, s0+5]
    volatility_range = [sigma/100, .1 + sigma/100]

    call_map, put_map = draw_options_heat_maps(10, spot_range, volatility_range, T, K, r)

    graph_result = [
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(figure=call_map)
                    ])
                )
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=put_map)
                    ])
                ])
            ])
        ])
    ]

    return call_result, put_result, graph_result


def draw_options_heat_maps(n: int, spot_range: list[int], volatility_range: list[float], T:int, K: int, r: float):
    spots = np.linspace(spot_range[0], spot_range[1], n)
    sigmas = np.linspace(volatility_range[0], volatility_range[1], n)
    bsm = BSM()

    call_map = np.array([[bsm.compute_bsm(s, K, r, T, sigma) for s in spots] for sigma in sigmas])
    put_map = np.array([[bsm.compute_bsm(s, K, r, T, sigma, is_call=False) for s in spots] for sigma in sigmas])

    call_fig = go.Figure(data=go.Heatmap(z=call_map, x=spots, y=sigmas, texttemplate="%{z:$.2f}"))
    put_fig = go.Figure(data=go.Heatmap(z=put_map, x=spots, y=sigmas, texttemplate="%{z:$.2f}"))

    return call_fig, put_fig


