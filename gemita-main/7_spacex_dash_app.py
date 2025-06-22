# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("4_spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


# TASK 1: Add dropdown list to enable Launch Site selection
site_options = [{'label': 'All Sites', 'value': 'ALL'}]
site_options += [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}), dcc.Dropdown(id='site-dropdown',options=site_options,
                                                                               value='ALL',placeholder='Select a Launch Site',searchable=True),
 
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload,max=max_payload,step=1000,
                                    marks={int(i): f'{int(i)}' for i in range(int(min_payload),int(max_payload)+ 1, 1000)},
                                    value=[min_payload, max_payload]),
                                html.Br(),
  
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(
            spacex_df[spacex_df['class'] == 1],
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Launch Outcomes for {selected_site}',
            labels={0: 'Failure', 1: 'Success'}
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(selected_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Success',
        labels={'class': 'Launch Outcome'}
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
