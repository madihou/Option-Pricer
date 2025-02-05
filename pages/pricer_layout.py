from BSM import BSM
from utils.data import DataManager
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, State, Output, dcc, html, callback

data = DataManager()


def create_pricer_layout():

    content_layout = [
        html.Div([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(id="call_result")
                    ], color="#27b744")
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(id="put_result")
                    ], color="#d66152")
                ])
            ]),
            html.Br(),
            dbc.Row([
                html.H3("Spot-Volatility Heat Map", className="display-9", style={"color": "rgb(255, 255, 255)"}),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.H6("Heat map size :", style={"color": "rgb(255, 255, 255)"})
                    ]),
                    dbc.Col([
                        dbc.Input(id="hm_size", type="number", min=5, value=10)
                    ]),
                ]),
                html.Br(),
                html.H6("Spot price range :", style={"color": "rgb(255, 255, 255)"}),
                dcc.RangeSlider(0, 0, 1, value=[0, 0], id="spot_range"),
                html.Br(),
                html.H6("Volatility range :", style={"color": "rgb(255, 255, 255)"}),
                dcc.RangeSlider(0, 0, .01, value=[0, 0], id="volatility_range")
            ]),
            html.Br(),
            html.Div(id="bsm_graph")
        ])
    ]
    
    sidebar_layout = [
            html.H3("BSM Parameters", className="display-9", style={"color": "rgb(255, 255, 255)"}),
            html.Hr(style={"color": "#d703d7", "border": "none", "border-radius": "10px", "border-top": "3px solid #d703d7", "width": "100%"}),
            html.H6("Spot:", style={"color": "rgb(255, 255, 255)"}),
            dbc.Input(id="spot_input", type="number"),
            html.Br(),
            html.H6("Strike:", style={"color": "rgb(255, 255, 255)"}),
            dbc.Input(id="strike_input", type="number"),
            html.Br(),
            html.H6("Maturity:", style={"color": "rgb(255, 255, 255)"}),
            dbc.Input(id="maturity_input", type="number", style={"color": "purple"}),
            html.Br(),
            html.H6("Risk-free rate:", style={"color": "rgb(255, 255, 255)"}),
            dbc.Input(id="rate_input", type="number", max=1, min=0, step=.01),
            html.Br(),
            html.H6("Volatility:", style={"color": "rgb(255, 255, 255)"}),
            dcc.Slider(id="volatility_slider", value=0, min=0, max=100,
                       tooltip={"always_visible": True, "template": "{value}%"}),
            dbc.Button(id="compute_button", children="Compute !"),
    ]
    
    return content_layout, sidebar_layout


@callback(
    Output("call_result", "children"),
    Output("put_result", "children"),
    Output("bsm_graph", "children"),
    Output("spot_range", "min"),
    Output("spot_range", "max"),
    Output("spot_range", "value"),
    Output("volatility_range", "min"),
    Output("volatility_range", "max"),
    Output("volatility_range", "value"),
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

    call_result = [html.H6("Call Price :", className="display-6"), html.H6(f"${c:.2f}", className="display-6")]
    put_result = [html.H6("Put Price :", className="display-6"), html.H6(f"${p:.2f}", className="display-6")]

    spot_range = [s0, s0+10]
    volatility_range = [sigma/100, .3 + sigma/100]

    call_map_fig, put_map_fig = draw_options_heat_maps(10, spot_range, volatility_range, T, K, r)

    graph_result = [
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Call Option Price Heat Map", style={"color": "rgb(255, 255, 255)"}),
                        dcc.Graph(figure=call_map_fig, id="call_map", config={"displayModeBar": False})
                    ])
                ], color="#302e32")
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Put Option Price Heat Map", style={"color": "rgb(255, 255, 255)"}),
                        dcc.Graph(figure=put_map_fig, id="put_map", config={"displayModeBar": False})
                    ])
                ], color="#302e32")
            ])
        ])
    ]
    data.dump_data(bsm)
    return call_result, put_result, graph_result, spot_range[0], spot_range[1], spot_range, volatility_range[0], volatility_range[1], volatility_range


@callback(
    Output("call_map", "figure"),
    Output("put_map", "figure"),
    Input("hm_size", "value"),
    Input("spot_range", "value"),
    Input("volatility_range", "value"),
    prevent_initial_call=True,
)
def update_heat_maps(n: int, spot_range: list[int], sigma_range: list[float]):
    bsm = data.load_data()
    call_map_fig, put_map_fig = draw_options_heat_maps(n, spot_range, sigma_range, bsm.maturity, bsm.strike, bsm.risk_free)

    return call_map_fig, put_map_fig


def draw_options_heat_maps(n: int, spot_range: list[int], volatility_range: list[float], T:int, K: int, r: float):
    spots = np.linspace(spot_range[0], spot_range[1], n)
    sigmas = np.linspace(volatility_range[0], volatility_range[1], n)
    bsm = BSM()

    call_map = np.array([[bsm.compute_bsm(s, K, r, T, sigma) for s in spots] for sigma in sigmas])
    put_map = np.array([[bsm.compute_bsm(s, K, r, T, sigma, is_call=False) for s in spots] for sigma in sigmas])

    call_fig = go.Figure(layout=go.Layout(template="plotly_dark", paper_bgcolor="#302e32", margin=dict(l=25, r=25, t=35, b=35)), data=go.Heatmap(z=call_map, x=spots, y=sigmas, texttemplate="%{z:$.2f}"))
    put_fig = go.Figure(layout=go.Layout(template="plotly_dark", paper_bgcolor="#302e32", margin=dict(l=25, r=25, t=35, b=35)), data=go.Heatmap(z=put_map, x=spots, y=sigmas, texttemplate="%{z:$.2f}"))

    return call_fig, put_fig
