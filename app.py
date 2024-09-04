from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from flask_restful import Api
from dotenv import load_dotenv

from io import StringIO

load_dotenv()

app = Dash()

from data_handler import DatabaseHandler, DatabaseServices
from date_handler import DatetimeHandler


api = Api(app.server)

api.add_resource(DatabaseHandler, '/save_number',)
api.add_resource(DatetimeHandler, '/get_time',)

app.layout = [
    html.H1(children='Random Generator behaviour', style={'textAlign':'center'}),
    dcc.Graph(id='graph-content-0'),
    dcc.Graph(id='graph-content-1'),
    dcc.Graph(id='graph-content-2'),
    dcc.Interval(id='refresh-data', interval=10000),
    dcc.Store(id='random-data')
]

@callback(Output('random-data', 'data'),Input('refresh-data', 'n_intervals'))
def update_graph(n_intervals):
    data = DatabaseServices.find()
    df = pd.DataFrame(list(data))
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df.to_dict()

@callback(Output('graph-content-0', 'figure'),Input('random-data', 'data'))
def update_graph(data):
    df = pd.DataFrame.from_dict(data)
    return px.histogram(df, x="htrng",)

@callback(Output('graph-content-1', 'figure'),Input('random-data', 'data'))
def update_graph(data):
    df = pd.DataFrame.from_dict(data)
    return px.density_heatmap(df, x="htrng")

@callback(Output('graph-content-2', 'figure'),Input('random-data', 'data'))
def update_graph(data):
    df = pd.DataFrame.from_dict(data)
    return px.scatter(df, x="timestamp", y=["adc", "htrng"])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)


