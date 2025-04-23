from dash import html, dcc
import plotly.express as px

def get_layout(
    data_df,
):
    return html.Div([
        html.H1("Fire Stats"),
        dcc.Graph(
            id = "fire-stats-prov",
            figure = px.bar(
                data_frame = data_df
            )
        ),
    ])