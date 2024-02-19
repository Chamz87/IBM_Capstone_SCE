import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

sites = spacex_df['Launch Site'].unique().tolist()
sites.insert(0, 'All Sites')

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': i, 'value': i} for i in sites],
        placeholder="Select a Launch Site here",
        value='All Sites',
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={i * 1000: f'{i * 1000} kg' for i in range(11)},
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def get_pie(value):
    filtered_df = spacex_df.copy()
    if value == 'All Sites':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    elif value in sites:
        filtered_df = filtered_df[filtered_df['Launch Site'] == value].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        title = f"Total Success Launches for site {value}"
        fig = px.pie(filtered_df, values='class count', names='class', title=title)
        return fig
    else:
        
        return px.pie()

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_scatter(value1, value2):
    filtered_df2_1 = spacex_df[(spacex_df['Payload Mass (kg)'] > value2[0]) & (spacex_df['Payload Mass (kg)'] < value2[1])]

    if value1 == 'All Sites':
        fig = px.scatter(filtered_df2_1, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for All sites")
        return fig
    elif value1 in sites:
        filtered_df2_2 = filtered_df2_1[filtered_df2_1['Launch Site'] == value1]
        title = f"Correlation between Payload and Success for site {value1}"
        fig = px.scatter(filtered_df2_2, x="Payload Mass (kg)", y="class", color="Booster Version Category", title=title)
        return fig
    else:
        
        return px.scatter()

if __name__ == '__main__':
    app.run_server()