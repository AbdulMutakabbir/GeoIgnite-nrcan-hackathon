from dash import Input, Output, State
import plotly.express as px
import pandas as pd


def get_callback(
    app,
    store,
    config,
    fig_gen,
):
    @app.callback(
        [
            Output("percentage-fire-stats-prov-id", "figure", allow_duplicate=True),
            Output("area-fire-stats-prov-id", "figure", allow_duplicate=True),
        ],
        Input("active-prov-selector", 'value'),
        prevent_initial_call=True,
    )
    def on_prov_select(prov):
        store.set_active_prov(prov)
        percent_fig = fig_gen["percentage-fire-stats-prov-id"](store = store)
        area_fig = fig_gen["area-fire-stats-prov-id"](store = store)
        return [percent_fig, area_fig]
