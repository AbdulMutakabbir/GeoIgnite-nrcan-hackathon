from dash import html, dcc
import plotly.express as px

def get_fig(
    store
):
    data_df = store.state['area_grown_after_fire_data']
    fig = fig = px.bar(
        data_frame=data_df, 
        x="year", 
        y=data_df.columns[1:], 
        barmode="stack",
        color_discrete_map=store.state['color_map'],
        text_auto='.2f',
    )
    fig.update_traces(
        textposition = 'inside', 
        hoverinfo = ['x', 'y', 'z', 'text', 'name'],
        # textinfo = 'label+percent entry',
        hovertemplate="%{value:.2f} km^2 of the total fuel type grown in 2024 from %{x} historic fire accounted for this <extra></extra>",
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
            title = "Yearly Fuel Type Grown in Km^2"
        ),
        xaxis=dict(
            title = "Year"
        ),
        margin=dict(t=0, b=0, l=0, r=0),
    )

    return fig

def get_layout(
    config,
    store,
):
    fig = get_fig(store=store)
    return html.Div([
        dcc.Graph(
            id = "area-fire-stats-prov-id",
            figure = fig
        ),
    ])