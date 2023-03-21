from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

"read data from excel into dataframe"  
df = pd.read_json('output/concise_output.json')


app.layout = html.Div([
    # html.Div([
    #     html.Div([
    #         html.Label(['Select x-value'], style={'font-weight': 'bold', "text-align": "right","offset":1}),], style=dict(width='33%')),
    #     html.Div([
    #         html.Label(['Select y-value'], style={'font-weight': 'bold', "text-align": "center"}),], style=dict(width='33%')),
    #     html.Div([
    #         html.Label(['Select size'], style={'font-weight': 'bold', "text-align": "left"}),], style=dict(width='33%'))
    #     ],
    #     style=dict(display='flex',justifyContent='center')),
    html.Div([
        html.Label(['Select x-value'], style={'font-weight': 'bold', "text-align": "right","offset":1}),    
        html.Div([
            dcc.Dropdown(
                df[
                    (df["Indicator Name"] != "points_time_series")
                    &(df["Indicator Name"] != "selected_time_series")
                ]['Indicator Name'].unique(),
                'value',
                id='crossfilter-xaxis-column',
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='crossfilter-xaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ])],
        style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Label(['Select y-value'], style={'font-weight': 'bold', "text-align": "right","offset":1}),   
        html.Div([
            dcc.Dropdown(
                df[
                    (df["Indicator Name"] != "points_time_series")
                    &(df["Indicator Name"] != "selected_time_series")
                ]['Indicator Name'].unique(),
                'season_points',
                id='crossfilter-yaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='crossfilter-yaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ])],
        style={'width': '33%', 'display': 'inline-block'}
    ),
    html.Div([
        html.Label(['Select size'], style={'font-weight': 'bold', "text-align": "right","offset":1}),    
        html.Div([
            dcc.Dropdown(
                df[
                    (df["Indicator Name"] != "points_time_series")
                    &(df["Indicator Name"] != "selected_time_series")
                ]['Indicator Name'].unique(),
                'season_points',
                id='crossfilter-size-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='crossfilter-yaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ])],
        style={'width': '33%', 'display': 'inline-block'}
    ),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Bukayo Saka'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    # html.Div(dcc.Slider(
    #     df['Value'].min(),
    #     df['Value'].max(),
    #     step=None,
    #     id='crossfilter-Value--slider',
    #     value=df['Value'].max(),
    #     marks={str(Value): str(Value) for Value in df['Value'].unique()}
    # ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-size-column', 'value')
    # Input('crossfilter-Value--slider', 'value')
    )

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, size
                 ):
    dff = df

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            size = tuple(dff[dff['Indicator Name'] == size]['Value']),
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['full_name'],
            trendline = "ols",
            )

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['full_name'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(df, axis_type, title):

    if title == "popularity":
        df = df[df["Indicator Name"] == "selected_time_series"]
        yaxis_title = "Selected"
    else:
        df = df[df["Indicator Name"] == "points_time_series"]
        yaxis_title = "Pts"
    
    y = df.iloc[0]["Value"]
    
    dff = pd.DataFrame (y, columns = ['points'])
    
    fig = px.scatter(dff, x=dff.index, y=dff['points'])

    fig.update_layout(
        xaxis_title="Gameweek",
        yaxis_title=yaxis_title
    )

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    Output('x-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'))
def update_points_timeseries(hoverData, xaxis_column_name, axis_type):
    full_name = hoverData['points'][0]['customdata']
    dff = df[df['full_name'] == full_name]
    df_time_series = df[df['full_name'] == full_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(full_name, "points vs match")
    return create_time_series(df_time_series, axis_type, title)


@app.callback(
    Output('y-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-type', 'value'))
def update_popularity_timeseries(hoverData, yaxis_column_name, axis_type):
    full_name = hoverData['points'][0]['customdata']
    dff = df[df['full_name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    df_time_series = df[df['full_name'] == full_name]
    return create_time_series(df_time_series, axis_type, "popularity")


if __name__ == '__main__':
    app.run_server(debug=True)

