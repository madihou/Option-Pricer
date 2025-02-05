import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from component.app_layout import sidebar, content
from dash import Dash, Input, Output, dcc, html, callback, _dash_renderer
from pages.pricer_layout import create_pricer_layout
from pages.delta_sim import create_delta_sim_layout
from pages.greeks_study import create_greek_layout
_dash_renderer._set_react_version("18.2.0")


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP] + dmc.styles.ALL)

app.layout = dmc.MantineProvider(html.Div([sidebar, content]))


@callback(
    Output("page_content", "children"),
    Output("sidebar", "children"),
    Input("content_tabs", "value")
)
def update_layout(tab_name):
    if tab_name == "pricer":
        return create_pricer_layout()
    if tab_name == "delta_sim":
        return create_delta_sim_layout()
    if tab_name == "greeks":
        return create_greek_layout()


if __name__ == "__main__":
    app.title = "BSM Option Pricer"
    app.run()#debug=True)
