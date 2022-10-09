import pandas as pd
import plotly.express as px
import dash_daq as daq
from dash import Dash, html, dcc, Input, Output
from PIL import Image
from datetime import datetime, timedelta

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}


app = Dash(__name__, 
          assets_external_path='assets/base-styles.css')

rootLayout = html.Div(style={'backgroundColor': '#6C6968'}, children = [ 
    html.H1(children='AEP'), 
    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(id = "slct_turbine",
                    options=[
                        {"label" : "Station A", "value": "stationOne.csv"},
                        {"label" : "Station B", "value": "Station B"},
                        {"label" : "Station C", "value": "Station C"},
                        {"label" : "Station D", "value": "Station D"},
                        {"label" : "Station E", "value": "Station E"},
                        {"label" : "Station F", "value": "Station F"},
                        {"label" : "Station G", "value": "Station G"},
                        {"label" : "Station H", "value": "Station H"},
                        {"label" : "Station I", "value": "Station I"},
                        {"label" : "Station J", "value": "Station J"}],
                    multi = False,
                    value = "stationOne.csv",

        )

    ]),  

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    
    html.Div(
                id="Wind",
                className='four columns',
                children=[
                    html.H5("Wind Direction"),
                    html.Img(id = "windDir", height = 50),
                    html.H5("Wind Speed"),
                    daq.LEDDisplay(
                        id = "windSpeed",
                        size=50,
                    )
                ]
            ),

             
    html.Div(
                id="power",
                children=[
                    daq.Gauge(
                        id='power-gauge',
                        label="Power",
                        size=150,
                        value = 0,
                        max = 100,
                        min=0
                    )
                ]
            ),

    dcc.Graph(id='pba', figure = {})
])

app.layout = html.Div(id='dark-theme-components-1', 
    children=[
        daq.DarkThemeProvider(theme=theme, children=rootLayout)
    ])


@app.callback(
    Output(component_id='pba', component_property='figure'),
    Output(component_id='windDir', component_property='src'),
    Output(component_id='windSpeed', component_property='value'),
    Output(component_id='power-gauge', component_property='value'),
    Output(component_id='power-gauge', component_property='max'),
    Input(component_id='slct_turbine', component_property='value')
)
def update_station(option_slctd):

    station = pd.read_csv(option_slctd)

    station["LOSS_PROD"] = station["EXPECTED POWER"] - station["POWER"]

    station["PRODUCTION_BASED_AVAILABLE"] = station["LOSS_PROD"] / (station["POWER"] + station["LOSS_PROD"])    
    
    station["Date & Time"] = pd.to_datetime(station["Date & Time"])

    # Production_Based_Available
    time_now = max(station["Date & Time"])
    range = time_now - timedelta(days = 30)
    fig = px.scatter(station[station["Date & Time"] > range], "Date & Time", "PRODUCTION_BASED_AVAILABLE")

    # Wind Dir
    windDir = station[station["Date & Time"] == time_now].iloc[0]["WIND DIRECTION"]
    arrow_img =  Image.open("assets/arrow.png")
    arrow_img = arrow_img.rotate(windDir)

    # Wind Speed
    windSpeed = station[station["Date & Time"] == time_now].iloc[0]["WIND SPEED"]
    windSpeed = round(windSpeed, 2)

    # Power
    power = station[station["Date & Time"] == time_now].iloc[0]["POWER"]
    power = round(power, 2)
    maxPower = round(max(station["POWER"]), 0)

    return fig, arrow_img, windSpeed, power, maxPower

if __name__ == '__main__':
    app.run_server(debug=True)


    