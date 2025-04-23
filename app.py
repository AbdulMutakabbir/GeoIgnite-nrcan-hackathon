from dash import Dash, html, dcc, callback, Output, Input
from flask import Flask, request
from flask_cors import CORS
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv
from src import layouts as layouts
from src import callbacks as callbacks
from src import processors as processors
import config

# Load environment variables from .env
load_dotenv(".env")
load_dotenv(".flaskenv")
PROV_COL_NAME = os.getenv("PROV_COL_NAME")
COUNT_COL_NAME = os.getenv("COUNT_COL_NAME")
FUEL_COL_NAME = os.getenv("FUEL_COL_NAME")

# prov_land_area_processor = processors.ProvFuelTypeLandAreaDataProcessor()
# prov_land_area_inner_ring_df = prov_land_area_processor.get_inner_ring_data()

# Create Dash app with custom Flask server
server = Flask(__name__)
CORS(server)  # Enable CORS on the Flask server

app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.title = "2024 Fuel Type Canada"

store = processors.Store()


# Requires Dash 2.17.0 or later
app.layout = [
    layouts.home_page.get_layout(

    ),
    dbc.Row(
        children = [
            dbc.Col(
                style = {"margin-left":"1rem"},
                children = [
                    dbc.Card(
                    [
                        dbc.CardBody(
                            style={
                                "align": "center", 
                                "font-size": "2rem", 
                                "height": "100%",
                            },
                            children = [
                                html.H4(
                                    children = "Distribution of Different Fuel Types by Province", 
                                    style={
                                        "text-align": "center", 
                                        "font-size": "2rem", 
                                    },
                                ),
                                layouts.dist_fuel_prov.get_layout(
                                    config = config.DistFuelProv,
                                    processor = prov_land_area_processor
                                )
                            ], 
                        ),
                    ],
                )
                ]
            ),
            dbc.Col(
                children = [
                    dbc.Row(
                        children = dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H1(  
                                            style={
                                                "text-align": "center", 
                                                "font-size": "2rem", 
                                            },
                                            children = "Percentage of Fuel Type Grown in each Year after Historic Fires",
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ),
                    dbc.Row(children = dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                        html.H1(  
                                            style={
                                                "text-align": "center", 
                                                "font-size": "2rem", 
                                            },
                                            children = "Fuel Type Grown in each Year after Historic Fires",
                                        ),
                                ]
                            ),
                        ],
                    ))
                ]
            ),
        ]
    ),
    # layouts.fire_stats_prov.get_layout(
    #     data_df = 
    # )
]


callbacks.dist_fuel_prov.get_callback(
    app = app,
    config = config,
)

if __name__ == "__main__":
    # Use environment variables or fallback defaults
    port = int(os.environ.get("PORT", 8050))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("DEBUG", "True") == "True"

    app.run(debug=debug, host=host, port=port)





