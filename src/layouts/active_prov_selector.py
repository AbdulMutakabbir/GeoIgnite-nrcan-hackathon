from dash import html
import plotly.express as px
import dash_bootstrap_components as dbc


def get_layout(
    config,
    store,
):
    return dbc.CardBody(
        style={
            "align": "center", 
            "font-size": "2rem", 
            "height": "100%",
        },
        children = [
            html.H4(
                children = "Current Active Region", 
                style={
                    "text-align": "center", 
                    "font-size": "2rem", 
                },
            ),
            dbc.Select(
                id="active-prov-slector",
                options = [ {"label": prov, "value": prov} for prov in store.state['prov_list'] ],
                value = store.state['active_prov']
            ),
        ], 
    )
