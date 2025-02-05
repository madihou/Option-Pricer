import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from BSM import BSM
from utils.data import DataManager
from plotly.subplots import make_subplots
from dash import Input, State, Output, dcc, html, callback


def create_greek_layout():

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
        dbc.Input(id="maturity_input", type="number"),
        html.Br(),
        html.H6("Risk-free rate:", style={"color": "rgb(255, 255, 255)"}),
        dbc.Input(id="rate_input", type="number", max=1, min=0, step=.01),
        html.Br(),
        html.H6("Volatility:", style={"color": "rgb(255, 255, 255)"}),
        dcc.Slider(id="volatility_slider", value=0, min=0, max=100,
                   tooltip={"always_visible": True, "template": "{value}%"}),
        html.Br(),
        html.H6("Option type:", style={"color": "rgb(255, 255, 255)"}),
        dcc.RadioItems(["Call", "Put"], "Call", inline=True, id="option_type", style={"color": "rgb(255, 255, 255)"}),
        html.Br(),
        dbc.Button(id="compute_button", children="Compute !"),
    ]

    content_layout = [
        html.Br(),
        html.Div([
            dbc.Card([
                dbc.CardBody([])
            ], color="#302e32"),
            html.Br(),
            dbc.Card([
                dbc.CardBody([
                    html.H6("Greeks plots", style={"color": "rgb(255, 255, 255)"}),
                    html.Br(),
                    dcc.Graph(id="greeks_plots", config={"displayModeBar": False})
                ])
            ], color="#302e32")
        ])
    ]

    return content_layout, sidebar_layout


@callback(
    Output("greeks_plots", "figure"),
    State("spot_input", "value"),
    State("strike_input", "value"),
    State("maturity_input", "value"),
    State("rate_input", "value"),
    State("volatility_slider", "value"),
    State("option_type", "value"),
    Input("compute_button", "n_clicks"),
    prevent_initial_call=True
)
def run_greeks(s0, K, T, r, sigma, option_type, _):
    is_call = True if option_type == "Call" else False
    bsm = BSM()
    bsm.initialize_bsm(s0, K, T, r, sigma)
    time = np.linspace(0, T, 50)
    greeks = pd.DataFrame(data=.0, columns=["Delta", "Gamma", "Theta", "Vega", "Rho"], index=time)
    greeks["Delta"] = bsm.compute_delta(s0, K, r, time, sigma, is_call)
    greeks["Gamma"] = bsm.compute_gamma(s0, K, r, time, sigma)
    greeks["Theta"] = bsm.compute_theta(s0, K, r, time, sigma, is_call)
    greeks["Vega"] = bsm.compute_vega(s0, K, r, time, sigma)
    greeks["Rho"] = bsm.compute_rho(s0, K, r, time, sigma, is_call)

    greeks_plot = draw_greeks_plot(greeks)

    return greeks_plot


def draw_greeks_plot(greeks: pd.DataFrame):
    title = ["∆", "Γ", "Θ", "V", "Ρ"]
    greeks_plot = make_subplots(rows=3, cols=2, subplot_titles=title)
    s = 0
    for j in range(2):
        for i in range(3):
            greeks_plot.add_traces(
                [go.Scatter(
                    x=greeks.index,
                    y=greeks[greeks.columns[s]],
                    name=title[s]
                )],
                rows=i+1,
                cols=j+1
            )
            s += 1
            if s == 5:
                break

    greeks_plot.update_layout(template="plotly_dark", paper_bgcolor="#302e32", plot_bgcolor="#302e32")
    greeks_plot.update_xaxes(showline=False, showgrid=False, linewidth=2, linecolor="#000000", gridcolor="#000000")
    greeks_plot.update_yaxes(showline=False, showgrid=False, linewidth=2, linecolor="#000000", gridcolor="#000000")
    return greeks_plot
