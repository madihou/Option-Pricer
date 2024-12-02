import dash_bootstrap_components as dbc
from .constant import SIDEBAR_STYLE, CONTENT_STYLE
from dash import html, dcc


sidebar = html.Div(
    [
        html.H3("Parameters", className="display-6"),
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
        dcc.Slider(id="volatility_slider", value=0, min=0, max=100, tooltip={"always_visible": True, "template": "{value}%"}),
        html.Br(),
        dbc.Button(id="compute_button", children="Compute !")
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [
        html.H3("Option Pricer", className="display-5"),
        html.Hr(),
        dcc.Tabs([
            dcc.Tab(label="Theoretical", id="theoretical_tab", value="theoretical"),
            dcc.Tab(label="Delta Hedge Simulation", id="real_time_tab", value="real_time")
        ], value="theoretical", id="content_tabs"),
        html.Div(id="page_content")
    ],
    style=CONTENT_STYLE
)
