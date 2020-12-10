import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from forecaster.predict import tft_pred

# Load data
df = tft_pred()
#df.index = df['month']

# Initialise the app
app = dash.Dash(__name__)

def get_options(list_items):
    dict_list = []
    for i in list_items:
        dict_list.append({'label': i, 'value': i})

    return dict_list

# Define the app
app.layout = html.Div(children=[
                        html.Div(className='row',  # Define the row element
                                children=[
                                    html.Div(className='four columns div-user-controls',  # Define the left element
                                            children = [
                                                html.H2('DEMAND FORECASTING using PyTorchForecasting'),
                                                html.P('''Pick one or more items from the dropdown below.'''),
                                                html.Div(className='div-for-dropdown',
                                                        children=[
                                                            dcc.Dropdown(id='itemselector',
                                                                            options=get_options(df['item'].unique()),
                                                                            multi=True,
                                                                            value=[df['item'].sort_values()[0]],
                                                                            style={'backgroundColor': '#1E1E1E'},
                                                                            className='itemselector')
                                                                ],
                                                            style={'color': '#1E1E1E'})
                                                        ]),
                                    
                                    html.Div(className='eight columns div-for-charts bg-grey',  # Define the right element
                                            children=[
                                                dcc.Graph(id='timeseries',
                                                config={'displayModeBar': False}, animate=True)
                                               
                                            ])
                                  ])
                        ])

@app.callback(Output('timeseries', 'figure'),
              [Input('itemselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for item in selected_dropdown_value:   
        trace.append(go.Scatter(x=df_sub[df_sub['item'] == item].month,
                                 y=df_sub[df_sub['item'] == item]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=item,
                                 textposition='bottom center'))  
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Demand Forecasts', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.month.min(), df_sub.month.max()], 'title': 'Month'},
                  yaxis={'title': 'Demand'}
              ),

              }

    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)