from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def get_callback(
    app,
    config
):
    @app.callback(
        Output("active-prov", 'children'),
        Input(config.DistFuelProv.ID, 'clickData'),
        prevent_initial_call=True
    )
    def on_prov_click(clickData):
        return clickData['points'][0]['label']