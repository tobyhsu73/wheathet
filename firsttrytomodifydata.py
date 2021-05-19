from datetime import datetime as dt
import pandas as pd
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app.title = "Zoe's FYP"
server = app.server

SHEET_ID='1SP5U7RmoU-_cDnrPJNAp2gkWDRq4bSE8JrOllBJzr9k'
df=pd.read_csv(F"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv")
latyear=df['year'].iloc[1]
latmon=df['month'].iloc[1]
latday=df['date'].iloc[1]
lattime=df['hour:minute'].iloc[1]
opts = [{'label' : i, 'value' : i} for i in df.iloc[:,1:6]]
day=df['year']+df['month']+df['date']+df['hour:minute']
date=df['year']+df['month']+df['date']



app.layout = html.Div(
    children=[
            html.Div(
                children=[
                    html.H1(
                        children="Dashboard",
                        style={ #'color': '#306E4E',
                                'fontsize': 12,
                                'font-weight': 'bold',
                                'text-align': 'left',
                                'margin': 10, }
                    ),
                ],
                className="header",
            ),
            html.Br(),
            html.P(['This dashboard shows the temperature, humidity and soil humidity in her room.',
                    html.Br(),
                    html.A("Click to download Zoe's Room Environment Data Source from Google Spreadsheets",
                                    href='https://docs.google.com/spreadsheets/d/1G25uhlL7FMViECb2COSXm-_ZPMHzgjqs_hjbOjQiays/export?format=csv',
                                    target='_blank')]),
            html.P(('Last Updated: ' + str(latyear) + str(latmon) + str(latday) + str(lattime) + '  UTC + 8'), style={'text-align': 'right'}),

            dcc.DatePickerRange(
                                id='my-date',
                                min_date_allowed=dt(2021, 1, 1),
                                max_date_allowed=dt(2025, 1, 1),
                                initial_visible_month=dt.today(),
                                #start_date=date.min(),
                                end_date=dt.today(),
                                ),
                                html.Div(id='output-date-range'),

            dcc.Dropdown(
                        id="ticker",
                        options=[{"label": x, "value": x}
                        for x in df.columns[4:]],
                        value=df.columns[1],
                        clearable=False,
                        ),
            dcc.Graph(id="time-series-chart"),


    ], style={'marginBottom': 50, 'marginTop': 25,'margin-left':50, 'margin-right':50}
)

@app.callback(
    Output("time-series-chart", "figure"),
    [Input("my-date", "start_date"),
     Input("my-date", "end_date"),
     Input("ticker", "value")])

def display_time_series(start_date, end_date, ticker):
    dff = df[(date > start_date) & (date < end_date)]
    fig = px.line(dff, x=day, y=ticker)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
