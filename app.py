import dash_bootstrap_components as dbc
from component.app_layout import sidebar, content
from dash import Dash, Input, Output, dcc, html, callback
from pages.theoretical_layout import create_theoretical_layout



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([sidebar, content])


@callback(
    Output("page_content", "children"),
    Input("content_tabs", "value")
)
def update_layout(tab_name):
    if tab_name == "theoretical":
        return create_theoretical_layout()


if __name__ == "__main__":
    app.title = "BSM Option Pricer"
    app.run()
