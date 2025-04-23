from dash import html, dcc
import plotly.express as px


def get_layout(
    config,
    processor,
):
    data_df = processor.get_data()
    fig = px.sunburst(
        data_frame = data_df, 
        path = config.DATA_DICT['path'], 
        values = config.DATA_DICT['value'],
        color = config.DATA_DICT['color'],
        color_discrete_map = processor.COLOR_MAP,
        height = config.CHART_DICT['height'],
        width = config.CHART_DICT['width'],
    )
    fig.update_traces(
        hoverinfo = 'label+text',
        textinfo = 'label+percent entry',
        hovertemplate="%{label}-> %{value:,.2f}km^2 of the total land area <extra></extra>",
    )
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    # fig = px.pie(
    #     data_frame = data_df,
    #     names = config.DATA_DICT['label'], 
    #     values = config.DATA_DICT['value'], 
    #     title = config.CHART_DICT['title'],
    #     hole = config.CHART_DICT['hole'],
    #     color_discrete_sequence=px.colors.sequential.Reds_r,
    #     width = config.CHART_DICT['width'],  
    #     height = config.CHART_DICT['height'],
    #     # sort = False,
    # )
    # fig.update_traces(
    #     textposition = 'inside', 
    #     hoverinfo = 'percent+label',
    #     textinfo = 'percent+label',
    #     hovertemplate="%{label}: %{percent} of the total fuel type land area <extra></extra>",
    #     showlegend = False,
    # )
    return html.Div([
        # html.H1(config.CHART_DICT['title']),
        dcc.Graph(
            id = config.ID,
            figure = fig
        ),
    ])


