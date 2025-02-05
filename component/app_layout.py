import dash_bootstrap_components as dbc
from .constant import SIDEBAR_STYLE, CONTENT_STYLE
from dash import html, dcc


sidebar = html.Div(
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [
        html.H3("Option Pricer", className="display-5", style={"color": "rgb(255, 255, 255)"}),
        html.Hr(style={"color": "#d703d7", "border": "none", "border-radius": "10px", "border-top": "3px solid #d703d7", "width": "100%"}),
        dcc.Tabs([
            dcc.Tab(label="Pricer", id="theoretical_tab", value="pricer"),
            dcc.Tab(label="Greeks", id="greeks", value="greeks"),
            dcc.Tab(label="Delta Hedge Simulation", id="delta_sim", value="delta_sim"),
        ], value="pricer", id="content_tabs"),
        html.Div(id="page_content")
    ],
    style=CONTENT_STYLE
)
