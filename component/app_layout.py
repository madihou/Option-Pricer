import dash_bootstrap_components as dbc
from .constant import SIDEBAR_STYLE, CONTENT_STYLE
from dash import html, dcc


sidebar = html.Div(
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [
        html.H3("Option Pricer", className="display-5"),
        html.Hr(),
        dcc.Tabs([
            dcc.Tab(label="Pricer", id="theoretical_tab", value="pricer"),
            dcc.Tab(label="Greeks", id="greeks", value="greeks"),
            dcc.Tab(label="Delta Hedge Simulation", id="delta_sim", value="delat_sim"),
        ], value="pricer", id="content_tabs"),
        html.Div(id="page_content")
    ],
    style=CONTENT_STYLE
)
