from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def get_callback(
    app,
    config,
    store,
    fig_gen
):
    @app.callback(
        [
            Output("percentage-fire-stats-prov-id", "figure", allow_duplicate=True),
            Output("area-fire-stats-prov-id", "figure", allow_duplicate=True),
            Output("active-prov-selector", "value", allow_duplicate=True)
        ],
        Input(config.DistFuelProv.ID, 'clickData'), 
        prevent_initial_call=True,
        allow_duplicate=True
    )
    def on_prov_click(clickData):
        prov = clickData['points'][0]['label']
        print(prov)
        store.set_active_prov(prov)
        percent_fig = fig_gen["percentage-fire-stats-prov-id"](store = store)
        area_fig = fig_gen["area-fire-stats-prov-id"](store = store)
        return [percent_fig, area_fig, prov]