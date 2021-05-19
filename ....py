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
print(date)




