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
        start_date=dt(2019, 1, 5),
        end_date=dt(2019, 1, 25)
    ),
    html.Div(id='output-container-date-picker-range'),
    html.Div([dcc.Graph(id="my-graph")]),
])

@app.callback(
    Output('my-graph','figure'),
    [Input('my-date-picker-range', 'start_date'), Input('my-date-picker-range', 'end_date')])
def update_figure(start_date, end_date):
    gdata = wd[(wd["DATE"] >= start_date) & (wd["DATE"] <= end_date)]
#    dff = df[(df["year"] >= year[0]) & (df["year"] <= year[1])]
    trace = []
    trace.append(go.Scatter(x=gdata["DATE"], y=gdata["Pollen Count"], name="Prediction", mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {"data": trace,"layout": go.Layout(title="Daily Predicted Pollen Counts", colorway=['#fdae61', '#abd9e9', '#2c7bb6'], yaxis={"title": "Temperature ( degree celsius )"}, xaxis={"title": "Date"})}
    
if __name__ == '__main__':
    app.run_server(debug=True)
