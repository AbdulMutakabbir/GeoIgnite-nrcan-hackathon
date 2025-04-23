from dash import html, dcc
import plotly.express as px

def get_layout(
    config,
    store,
):
    data_df = store.state['percent_grown_after_fire_data']
    fig = px.bar(
        data_frame = data_df, 
        x = "year", 
        y = data_df.columns[1:],
        text_auto = ".2f",
        barmode="stack",
        color_discrete_map=store.state["color_map"],
    )
    fig.update_traces(
        textposition = 'inside', 
        hoverinfo = ['x', 'y', 'z', 'text', 'name'],
        # textinfo = 'label+percent entry',
        hovertemplate="%{text} %{value:.2f}% of the total fuel type grown in 2024 after %{x} historic fire accounted for <extra></extra>",
        # showlegend = False,
    )
    fig.update_layout(
        legend=dict(
            title=None,  # Remove legend title
            orientation="h",
            yanchor="bottom",
            x=0.5,
            y=-0.35,  # adjust as needed
            xanchor="center",
        ),
        yaxis=dict(
            title = "Yearly Fuel Type Grown %"
        ),
        xaxis=dict(
            title = "Year"
        ),
        margin=dict(t=0, b=0, l=0, r=0),
    )
    return html.Div([
        dcc.Graph(
            id = "fire-stats-prov",
            figure = fig
        ),
    ])