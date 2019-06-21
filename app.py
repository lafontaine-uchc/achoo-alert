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
#app = dash.Dash(__name__, server=server)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
wd= pd.read_csv("./weatherTest.csv")
forecast = pd.read_csv("./app_data.csv")
wd["Pollen Count"] = wd.GDDSUM*6.69977761+wd.Doy*(-0.76507818)+39.26186356797564

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Pollen Predictor'),

    html.Div(children='''
        A web application for predicting pollen counts.
    '''),

    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(2019, 1, 1),
        max_date_allowed=dt(2019, 12, 30),
        start_date=dt(2019, 2, 1),
        end_date=dt(2019, 2, 7)
    ),
    html.Div(id='output-container-date-picker-range'),
    html.Div([dcc.Graph(id="my-graph")]),
    html.Div([dcc.Graph(id="my-graph2")])
])

@app.callback(
    Output('my-graph','figure'),
    [Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date')])
def update_figure(start_date, end_date):
    gdata = forecast[(forecast["DATE"] >= start_date) & (forecast["DATE"] <= end_date)]
#    dff = df[(df["year"] >= year[0]) & (df["year"] <= year[1])]
    trace = []
    trace.append(go.Scatter(x=gdata["DATE"], y=gdata["Pollen_Count"], name="Prediction", mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": trace,"layout": go.Layout(title="Daily Predicted Pollen Counts", colorway=['#fdae61', '#abd9e9', '#2c7bb6'], yaxis={"title": "Pollen Count"}, xaxis={"title": "Date"})}
 
@app.callback(
    dash.dependencies.Output('my-graph2', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_figure2(start_date, end_date):
    colors = {"Absent": 'blue',
              "Low":'darkgreen',
          "Moderate": 'lightgreen',
          "High": 'orange',
          "Very High": 'red'
          }
    
    dff = forecast[(forecast["DATE"] >= start_date) & (forecast["DATE"] <= end_date)]
    #trace1 = go.Bar(x=dff['DATE'], y=dff["Pollen_Count"], name="Prediction", marker={'color': colors[dff['pc_binned']]})
    bars = []
    for label, label_df in dff.groupby('pc_binned'):
        bars.append(go.Bar(x=label_df.DATE,
                           y=label_df.Pollen_Count,
                           name=label,
                           marker={'color': colors[label]}))
    return {
        'data': bars,
        'layout': go.Layout(title=f'Daiily Predicted Pollen Count',
                           # colorway=["#EF963B", "#EF533B"],
                                      hovermode="closest",
                            xaxis={'title': "Date", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 9, 'color': 'black'}},
                            yaxis={'title': "Daily Pollen Count", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'},'type':'log'},
                            shapes= [
#                                        # Line Vertical
#                                        {
#                                            'type': 'line',
#                                            'x0': 1,
#                                            'y0': 0,
#                                            'x1': 1,
#                                            'y1': 2,
#                                            'line': {
#                                                'color': 'rgb(55, 128, 191)',
#                                                'width': 3,}
#                                        },
                                                    # Line Horizontal
                                        {
                                            'type': 'line',
                                            'x0': start_date,
                                            'y0': 1500,
                                            'x1': end_date,
                                            'y1': 1500,
                                            'line': {
                                                'color': 'orange',
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
                                                'color': 'lightgreen',
                                                'width': 4,
                                                'dash': 'dash',
                                            }
                                        },
#                                        {
#                                            'type': 'line',
#                                            'x0': start_date,
#                                            'y0': 15,
#                                            'x1': end_date,
#                                            'y1': 15,
#                                            'line': {
#                                                'color': 'lightgreen',
#                                                'width': 4,
#                                                'dash': 'dot',
#                                            }
#                                        },
                                    ]
        )}  
                                                                                               
if __name__ == '__main__':
    app.run_server(debug=True)
