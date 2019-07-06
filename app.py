# -*- coding: utf-8 -*-
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import flask

server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
forecast = pd.read_csv("./app_data.csv")

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Achoo Alert'),

    html.H6(children='''
        Seasonal Allergy Planner
    '''),

    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(2019, 1, 1),
        max_date_allowed=dt(2019, 12, 30),
        start_date=dt(2019, 2, 1),
        end_date=dt(2019, 2, 7)
    ),
    html.Div(id='output-container-date-picker-range'),
    html.Div([dcc.Graph(id="pollen-count-graph")])
])

@app.callback(
    dash.dependencies.Output('pollen-count-graph', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_pollen_count_graph(start_date, end_date):
    colors = {"Absent": 'darkgreen',
              "Low":'blue',
              "Moderate": 'lightgreen',
              "High": 'orange',
              "Very High": 'red'
              }
    
    #trims graph data by selected time range    
    graph_data = forecast[(forecast["DATE"] >= start_date) & (forecast["DATE"] <= end_date)]
    #Creates different color bars for each pollen count threshold    
    bars = []
    for label, label_df in graph_data.groupby('pc_binned'):
        bars.append(go.Bar(x=label_df.DATE,
                           y=label_df.Pollen_Count,
                           name=label,
                           marker={'color': colors[label]}))
    #returns data and layout of figure to be used for pollen-count-graph
    return {
        'data': bars,
        'layout': go.Layout(title={'text': "Daily Pollen Count",
                                   'font': {'color': 'black', 'size': 28, }},
                            hovermode="closest",
                            xaxis={'title': "Date", 
                                   'titlefont': {'color': 'black', 'size': 18},
                                   'tickfont': {'size': 14, 'color': 'black'}},
                            yaxis={'title': "Daily Pollen Count",
                                   'titlefont': {'color': 'black', 'size': 18,},
                                   'tickfont': {'size': 14,'color': 'black'},
                                   'type':'log'},

                            #Adds threshold lines to the graph
                            shapes= [
                                        {
                                            'type': 'line',
                                            'x0': start_date,
                                            'y0': 1500,
                                            'x1': end_date,
                                            'y1': 1500,
                                            'line': {
                                                'color': 'red',
                                                'width': 4,
                                                'dash': 'dash',
                                            }
                                        },
                                        {
                                            'type': 'line',
                                            'x0': start_date,
                                            'y0': 90,
                                            'x1': end_date,
                                            'y1': 90,
                                            'line': {
                                                'color': 'orange',
                                                'width': 4,
                                                'dash': 'dash',
                                            }
                                        },
                                    ]
        )}  
                                                                                               
if __name__ == '__main__':
    app.run_server(debug=True)
