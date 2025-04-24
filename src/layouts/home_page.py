from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

def get_layout():

    citation = """
    @inproceedings{mutakabbir2025iri,
        author={Mutakabbir, Abdul and Lung, Chung-Horng and Naik, Kshirasagar and Zaman, Marzia and Purcell, Richard and Sampalli, Srinivas and Ravichandran, Thambirajah},
        booktitle={IEEE 26th International Conference on Information Reuse and Integration for Data Science}, 
        title={A Visual Statistical Insight into the Post-Wildfire Growth of Different Fuel Types in Canada}, 
        year={2025},
        pages={},
        doi={}
    }
    """
    return html.Div(
        children = [
            dbc.Row(
                children = [
                    dbc.Col(
                        children = [
                            html.P(
                                children = "A Visual Statistical Insight into the Post-Wildfire Growth of Different Fuel Types in Canada",
                                style = {
                                    "margin-left": "2rem", 
                                    "margin-right": "2rem", 
                                    "margin-top": "10rem", 
                                    "margin-bottom": "5rem",
                                    "text-align": "center", 
                                    # "margin": "auto", 
                                    "font-size": "5rem", 
                                    # "height": "100%",
                                }
                            ),
                        ],
                    ),
                ]
            ),
            dbc.Row(
                children = [
                    dbc.Col(
                        # width = 10,
                        # offset = 1,
                        style = {
                            "margin-left": "2rem", 
                            "margin-right": "2rem", 
                            "margin-top": "5rem", 
                            "margin-bottom": "5rem",
                        },
                        children = [
                            dbc.Accordion(
                                [
                                    dbc.AccordionItem(
                                        "I would like to thank GeoIgnite 2025 NRCan (CCMEO) GEO.ca Hackathon for allowing the participation in this hackathon. " \
                                        "This work has been inspired from our reseach paper submited to IRI 2025 conference and is currently under review.", 
                                        title="Acknowledgement"
                                    ),
                                    dbc.AccordionItem(
                                        title="Citation / Reference",
                                        children = [
                                            html.Pre(
                                                html.Code(citation)
                                            ),
                                        ], 
                                    ),
                                ],
                                start_collapsed = False,
                            ),
                        ]
                    )
                ]
            )
        ]
    )
