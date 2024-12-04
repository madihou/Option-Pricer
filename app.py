import dash_bootstrap_components as dbc
from component.app_layout import sidebar, content
from dash import Dash, Input, Output, dcc, html, callback
from pages.pricer_layout import create_pricer_layout



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([sidebar, content])


@callback(
    Output("page_content", "children"),
    Output("sidebar", "children"),
    Input("content_tabs", "value")
)
def update_layout(tab_name):
    if tab_name == "pricer":
        return create_pricer_layout()


if __name__ == "__main__":
    app.title = "BSM Option Pricer"
    app.run()
