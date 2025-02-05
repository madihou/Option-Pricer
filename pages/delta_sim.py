import numpy as np
import pandas as pd
import dash_ag_grid as dag
import plotly.graph_objects as go
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from BSM import BSM
from utils.data import DataManager
from dash_iconify import DashIconify
from dash import Input, State, Output, dcc, html, callback, _dash_renderer
_dash_renderer._set_react_version("18.2.0")

data = DataManager()


def create_delta_sim_layout():

    sidebar_layout = [
        html.Div([
            html.H3("Option Inputs", style={"color": "rgb(255, 255, 255)"}),
            html.Hr(),
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
            html.H6("Option type:", style={"color": "rgb(255, 255, 255)"}),
            dcc.RadioItems(["Call", "Put"], "Call", inline=True, id="option_type", style={"color": "rgb(255, 255, 255)"}),
            html.Hr(),
            html.H3("∆ Hedge Simulation Parameters", style={"color": "rgb(255, 255, 255)"}),
            html.Br(),
            html.H6("Number of shares:", style={"color": "rgb(255, 255, 255)"}),
            dbc.Input(id="shares_input", type="number"),
            html.Br(),
            html.H6("Timescale:", style={"color": "rgb(255, 255, 255)"}),
            dcc.RadioItems(["Daily", "Weekly"], "Daily", inline=True, id="hedging_timescale", style={"color": "rgb(255, 255, 255)"}),
            html.Br(),
            html.H6(id="hedging_timescale_text", style={"color": "rgb(255, 255, 255)"}),
            dbc.Input(id="simulation_period_input", type="number"),
            html.Br(),
            dbc.Button(id="run_button", children="Run Simulation!")
        ])
    ]

    content_layout = [
        html.Br(),
        dbc.Card([
            dbc.CardBody([
                dmc.Group([
                    html.H6("Spot price simulation", style={"color": "rgb(255, 255, 255)"}),
                    dmc.ActionIcon(DashIconify(icon="material-symbols:forward-media", width=20), variant="filled", size="lg", id="reload")
                ]),
                html.Br(),
                dcc.Graph(id="spot_simulation", config={"displayModeBar": False})
            ])
        ], color="#302e32"),
        html.Br(),
        html.Div(id="simulation_result")
    ]

    return content_layout, sidebar_layout


@callback(
    Output("spot_simulation", "figure", allow_duplicate=True),
    Output("simulation_result", "children"),
    State("spot_input", "value"),
    State("strike_input", "value"),
    State("maturity_input", "value"),
    State("rate_input", "value"),
    State("volatility_slider", "value"),
    State("option_type", "value"),
    State("shares_input", "value"),
    State("simulation_period_input", "value"),
    State("hedging_timescale", "value"),
    Input("run_button", "n_clicks"),
    prevent_initial_call=True
)
def run_simulation(s0: int, K: int, T: int, r: float, sigma: float, option_type: str, n_shares: int, period: int, timescale: str, _: int):
    """

    """
    is_call = True if option_type == "Call" else False
    scale_names = {"Daily": "Day", "Weekly": "Week"}

    bsm = BSM()
    bsm.initialize_bsm(s0, K, T, r, sigma / 100)
    bsm.compute_spot_price(timescale, period)

    fig = draw_spot_simulation(bsm.price, period)
    data.dump_data(bsm)

    _df = create_hedging_df(bsm, period, n_shares, is_call)
    _df.rename(columns={"index": scale_names[timescale]}, inplace=True)

    _cols = [
        {"field": col_name} for col_name in _df.columns
    ]

    grid = dag.AgGrid(
        id="hedging_table",
        columnDefs=_cols,
        rowData=_df.to_dict("records")
    )
    result_layout = [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody()
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody()
                ])
            ]),
        ]),
        html.Br(),
        grid
    ]
    return fig, result_layout


@callback(
    Output("spot_simulation", "figure", allow_duplicate=True),
    Output("hedging_table", "rowData"),
    State("simulation_period_input", "value"),
    State("hedging_timescale", "value"),
    State("option_type", "value"),
    State("shares_input", "value"),
    Input("reload", "n_clicks"),
    prevent_initial_call=True
)
def update_spot_simulation(period: int, timescale: str, option_type: str, n_shares: int, _: int):
    is_call = True if option_type == "Call" else False
    scale_names = {"Daily": "Day", "Weekly": "Week"}

    bsm = data.load_data()
    bsm.compute_spot_price(timescale, period)

    fig = draw_spot_simulation(bsm.price, period)
    _df = create_hedging_df(bsm, period, n_shares, is_call)
    _df.rename(columns={"index": scale_names[timescale]}, inplace=True)

    return fig, _df.to_dict("records")


@callback(
    Output("hedging_timescale_text", "children"),
    Input("hedging_timescale", "value")
)
def update_hedging_timescale_text(timescale: str):
    if timescale == "Daily":
        return "Number of days: "
    elif timescale == "Weekly":
        return "Number of weeks: "


def draw_spot_simulation(spot: list[np.array], period: int):
    spot_fig = go.Figure()
    t = np.arange(period+1)
    spot_fig.add_trace(
        go.Scatter(
            x=t,
            y=spot
        )
    )
    spot_fig.update_layout(template="plotly_dark", paper_bgcolor="#302e32", plot_bgcolor="#302e32", margin=dict(l=10, r=10, t=20, b=20))
    return spot_fig


def create_hedging_df(bsm_model: BSM, period: int, n_shares: int, is_call: bool):
    _cols = ["Stock Price", "Delta", "Shares Purchased", "Cost"]
    t = np.arange(period + 1)
    _df = pd.DataFrame(data=.0, columns=_cols, index=t)

    _df["Stock Price"] = bsm_model.price
    _df["Delta"] = bsm_model.compute_delta(bsm_model.price,
                                           bsm_model.strike,
                                           bsm_model.risk_free,
                                           bsm_model.period,
                                           bsm_model.volatility,
                                           is_call)
    _df["Shares Purchased"] = (_df["Delta"] - _df["Delta"].shift(1, fill_value=0)) * n_shares
    _df["Cost"] = _df["Shares Purchased"] * _df["Stock Price"]

    _df.reset_index(inplace=True)
    return _df
